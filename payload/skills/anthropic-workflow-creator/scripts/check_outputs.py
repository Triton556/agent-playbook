"""Deterministic observations of existing outputs. No execution or model calls."""
import json
import re
import sys
from pathlib import Path, PureWindowsPath

LIMIT = 8 * 1024 * 1024


def linked(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def checked_path(root, value):
    if not isinstance(value, str) or not value:
        raise ValueError("path must be a nonempty relative string")
    value = value.replace("\\", "/")
    rel = Path(value)
    if rel.is_absolute() or PureWindowsPath(value).drive or ".." in rel.parts or ":" in value:
        raise ValueError("absolute paths, parent traversal and alternate streams are forbidden")
    current = root
    for part in rel.parts:
        current = current / part
        if linked(current):
            raise ValueError("links and junctions are forbidden")
    current.resolve().relative_to(root)
    return current


def pointer_value(data, pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
        raise ValueError("pointer must be an RFC 6901 JSON pointer")
    if not pointer:
        return data
    for raw in pointer[1:].split("/"):
        # Reject malformed escapes rather than silently accepting them.
        if re.search(r"~(?![01])", raw):
            raise ValueError("invalid JSON pointer escape")
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(data, list):
            if not token.isdigit() or (len(token) > 1 and token.startswith("0")):
                raise KeyError(token)
            data = data[int(token)]
        elif isinstance(data, dict):
            data = data[token]
        else:
            raise KeyError(token)
    return data


def run(spec, root):
    if not isinstance(spec, dict) or not isinstance(spec.get("checks"), list) or not spec["checks"]:
        raise ValueError("checks must be a nonempty list")
    prepared = []
    for check in spec["checks"]:
        if not isinstance(check, dict) or not isinstance(check.get("text"), str) or not check["text"].strip():
            raise ValueError("each check needs nonempty text")
        kind = check.get("kind")
        if kind not in {"file_nonempty", "text_contains", "json_equals"}:
            raise ValueError("unsupported check kind")
        if kind == "text_contains" and (not isinstance(check.get("expected"), str) or not check["expected"]):
            raise ValueError("text_contains needs nonempty expected text")
        if kind == "json_equals":
            if "expected" not in check:
                raise ValueError("json_equals needs expected")
            ptr = check.get("pointer", "")
            if not isinstance(ptr, str) or not ptr.startswith("/") and ptr != "":
                raise ValueError("invalid JSON pointer")
            if re.search(r"~(?![01])", ptr):
                raise ValueError("invalid JSON pointer escape")
        prepared.append((check, checked_path(root, check.get("path"))))
    results = []
    for check, path in prepared:
        passed = False
        try:
            if not path.is_file():
                evidence = "File absent or not a regular file"
            elif path.stat().st_size > LIMIT:
                raise ValueError("selected file exceeds 8 MiB limit")
            elif check["kind"] == "file_nonempty":
                passed = path.stat().st_size > 0
                evidence = f"File length: {path.stat().st_size} bytes"
            elif check["kind"] == "text_contains":
                content = path.read_text(encoding="utf-8")
                passed = check["expected"] in content
                evidence = "Expected text found" if passed else "Expected text absent"
            else:
                data = json.loads(path.read_text(encoding="utf-8"))
                actual = pointer_value(data, check.get("pointer", ""))
                # JSON booleans and numbers are different kinds of values.
                passed = type(actual) is type(check["expected"]) and actual == check["expected"]
                evidence = "Value at requested pointer matches" if passed else "Value at requested pointer differs"
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, IndexError) as exc:
            evidence = f"Cannot verify assertion: {type(exc).__name__}"
        results.append({"text": check["text"], "passed": passed,
                        "evidence": f"{check['path']}: {evidence}"})
    passed_count = sum(item["passed"] for item in results)
    return {"mode": "local deterministic assertions; not an LLM benchmark",
            "expectations": results,
            "summary": {"passed": passed_count, "failed": len(results) - passed_count,
                        "total": len(results), "pass_rate": passed_count / len(results)}}


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python check_outputs.py <checks.json> <existing-output-directory>")
        base = Path(sys.argv[2])
        if linked(base) or not base.is_dir():
            raise ValueError("output directory must exist and cannot be a link or junction")
        # Reject link/junction ancestors as well as paths inside the root.
        if any(linked(parent) for parent in base.absolute().parents):
            raise ValueError("output directory has a link/junction ancestor")
        result = run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), base.resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["summary"]["failed"] == 0 else 1)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(2)
