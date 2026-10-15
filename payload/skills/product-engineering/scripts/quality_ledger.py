"""Local, read-only quality-evidence validator. Python standard library only.

This verifies a declared contract and evidence freshness, not visual judgment or
the truth of a reviewer's observation. No generator, shell, network or model call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from datetime import datetime

ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
HASH = re.compile(r"^[a-f0-9]{64}$")
KINDS = {"technical", "semantic", "visual", "human"}
MAX_JSON = 2 * 1024 * 1024


class LedgerError(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise LedgerError(message)


def text(value, label):
    need(isinstance(value, str) and bool(value.strip()) and len(value) <= 8000,
         label + " must be a nonempty bounded string")


def identifier(value, label):
    need(isinstance(value, str) and bool(ID.fullmatch(value)), "Invalid " + label)


def sequence(value, label):
    need(isinstance(value, list) and len(value) <= 5000, label + " must be a bounded list")


def unique_rows(value, label):
    sequence(value, label)
    result = {}
    for row in value:
        need(isinstance(row, dict), label + " rows must be objects")
        identifier(row.get("id"), label + ".id")
        need(row["id"] not in result, "Duplicate " + label + ".id: " + row["id"])
        result[row["id"]] = row
    return result


def safe_path(root, relative):
    text(relative, "path")
    # Forward slashes keep ledgers portable; Windows drives/UNC are rejected too.
    need(not relative.startswith(("/", "\\")) and ":" not in relative and "\\" not in relative,
         "Paths must be relative, forward-slash paths")
    parts = Path(relative).parts
    need(".." not in parts, "Parent traversal is not allowed")
    candidate = (root / relative).resolve(strict=True)
    need(candidate.is_relative_to(root), "Path escapes root: " + relative)
    need(candidate.is_file(), "Path is not a file: " + relative)
    return candidate


def sha_file(file):
    digest = hashlib.sha256()
    with file.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root, paths):
    root = Path(root).resolve(strict=True)
    need(root.is_dir(), "Root must be a directory")
    need(len(set(paths)) == len(paths) and bool(paths), "Snapshot paths must be unique and nonempty")
    rows = [{"path": p, "sha256": sha_file(safe_path(root, p))} for p in sorted(paths)]
    return {"files": rows, "digest": subject_digest(rows)}


def subject_digest(files):
    canonical = [{"path": row["path"], "sha256": row["sha256"]}
                 for row in sorted(files, key=lambda row: row["path"])]
    return hashlib.sha256(json.dumps(canonical, separators=(",", ":"), ensure_ascii=False)
                          .encode("utf-8")).hexdigest()


def image_size(file):
    """Read PNG/JPEG dimensions, not pixels; image content still needs inspection."""
    with file.open("rb") as handle:
        start = handle.read(24)
        if start[:8] == b"\x89PNG\r\n\x1a\n" and start[12:16] == b"IHDR":
            return struct.unpack(">II", start[16:24])
        need(start[:2] == b"\xff\xd8", "View must be PNG or JPEG: " + str(file))
        handle.seek(2)
        while True:
            marker = handle.read(1)
            need(bool(marker), "JPEG dimensions missing")
            if marker != b"\xff":
                continue
            while marker == b"\xff":
                marker = handle.read(1)
            need(bool(marker), "Truncated JPEG")
            code = marker[0]
            if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
                continue
            need(code not in (0xD9, 0xDA), "JPEG dimensions missing")
            raw = handle.read(2)
            need(len(raw) == 2, "Truncated JPEG segment")
            length = struct.unpack(">H", raw)[0]
            need(length >= 2, "Invalid JPEG segment")
            if code in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                raw = handle.read(5)
                need(len(raw) == 5, "Truncated JPEG dimensions")
                height, width = struct.unpack(">HH", raw[1:5])
                return width, height
            handle.seek(length - 2, 1)


def validate(data, root):
    root = Path(root).resolve(strict=True)
    report = {"schema_version": 1, "schema_valid": False, "ready_to_complete": False,
              "completion_rejected": False, "blockers": [], "advisories": [],
              "requirements": [], "evidence": [], "preserved": []}
    blockers, advisories = report["blockers"], report["advisories"]
    try:
        need(root.is_dir(), "Root must be a directory")
        need(isinstance(data, dict) and data.get("schema_version") == 1, "Unsupported ledger schema")
        task = data.get("task")
        need(isinstance(task, dict), "task must be an object")
        identifier(task.get("id"), "task.id")
        need(task.get("status") in {"in_progress", "blocked", "ready", "complete"}, "Invalid task.status")
        contract = data.get("contract")
        need(isinstance(contract, dict), "contract must be an object")
        for key in ("objective", "style", "functional", "context"):
            text(contract.get(key), "contract." + key)
        subjects = unique_rows(data.get("subjects"), "subjects")
        requirements = unique_rows(data.get("requirements"), "requirements")
        evidence = unique_rows(data.get("evidence"), "evidence")
        issues = unique_rows(data.get("issues"), "issues")
        need(bool(subjects) and bool(requirements), "At least one subject and requirement are needed")
        need(any(r.get("blocking") is True for r in requirements.values()), "At least one blocking requirement is needed")
        preserve = data.get("preserve", [])
        sequence(preserve, "preserve")

        def check_files(rows, label):
            sequence(rows, label)
            need(bool(rows), label + " must have at least one file")
            seen, failures = set(), []
            for row in rows:
                need(isinstance(row, dict), label + " rows must be objects")
                p = row.get("path")
                text(p, label + ".path")
                need(p not in seen, "Duplicate file path in " + label)
                seen.add(p)
                h = row.get("sha256")
                need(isinstance(h, str) and bool(HASH.fullmatch(h)), "Invalid SHA-256 in " + label)
                try:
                    if sha_file(safe_path(root, p)) != h:
                        failures.append("hash changed: " + p)
                except (LedgerError, OSError) as error:
                    failures.append(str(error))
            return failures

        digests, subject_current = {}, {}
        for sid, subject in subjects.items():
            failures = check_files(subject.get("files"), "subject " + sid)
            # Digest uses the approved snapshot, while changed actual files block completion.
            digests[sid] = subject_digest(subject["files"])
            subject_current[sid] = not failures
            blockers.extend("subject " + sid + ": " + f for f in failures)

        def subject_ids(row, label):
            ids = row.get("subject_ids")
            sequence(ids, label + ".subject_ids")
            need(bool(ids) and len(set(ids)) == len(ids), label + " needs unique subjects")
            need(all(isinstance(i, str) and i in subjects for i in ids), "Unknown subject in " + label)
            return ids

        valid_evidence, evidence_views = {}, {}
        for eid, item in evidence.items():
            need(item.get("kind") in KINDS, "Invalid evidence.kind")
            need(item.get("verdict") in {"pass", "fail", "observed"}, "Invalid evidence.verdict")
            text(item.get("method"), "evidence.method")
            text(item.get("observation"), "evidence.observation")
            reviewer = item.get("reviewer")
            need(isinstance(reviewer, dict) and reviewer.get("kind") in {"automated", "agent", "human"}, "Invalid reviewer")
            text(reviewer.get("name"), "reviewer.name")
            if item["kind"] == "human":
                need(reviewer["kind"] == "human", "Human evidence needs a human reviewer")
            if item["kind"] in {"visual", "human"}:
                need(item.get("inspected") is True, "Visual/human evidence needs inspected=true")
            observed = item.get("observed_at")
            text(observed, "evidence.observed_at")
            try:
                timestamp = datetime.fromisoformat(observed.replace("Z", "+00:00"))
                need(timestamp.tzinfo is not None, "Evidence time needs a timezone")
            except ValueError as error:
                raise LedgerError("Invalid evidence.observed_at") from error
            inputs = item.get("subject_hashes")
            need(isinstance(inputs, dict) and bool(inputs), "Evidence needs subject_hashes")
            need(all(sid in subjects and isinstance(h, str) and bool(HASH.fullmatch(h))
                     for sid, h in inputs.items()), "Invalid evidence subject hash")
            failures = check_files(item.get("files"), "evidence " + eid)
            failures += ["stale subject revision: " + sid for sid, h in inputs.items()
                         if digests[sid] != h or not subject_current[sid]]
            views = unique_rows(item.get("views", []), "evidence.views")
            view_set = set()
            for vid, view in views.items():
                sid = view.get("subject_id")
                need(sid in inputs, "View subject not bound to evidence input")
                p = view.get("path")
                need(any(f["path"] == p for f in item["files"]), "View file missing from hashed evidence")
                for field in ("width", "height"):
                    need(type(view.get(field)) is int and view[field] > 0, "Invalid view dimension")
                try:
                    size = image_size(safe_path(root, p))
                    if size != (view["width"], view["height"]):
                        failures.append("declared view dimensions differ from file: " + vid)
                except (LedgerError, OSError, struct.error) as error:
                    failures.append(str(error))
                view_set.add((sid, vid, view["width"], view["height"]))
            valid_evidence[eid] = not failures
            evidence_views[eid] = view_set
            report["evidence"].append({"id": eid, "fresh": not failures, "problems": failures})
            if failures:
                advisories.append("Evidence " + eid + " unusable: " + "; ".join(failures))

        allowed = {"technical": {"technical"}, "semantic": {"semantic", "human"},
                   "visual": {"visual", "human"}, "human": {"human"}}

        def usable(ids, sids, kind):
            sequence(ids, "evidence_ids")
            need(len(set(ids)) == len(ids) and all(e in evidence for e in ids), "Unknown/duplicate evidence reference")
            selected = [evidence[e] for e in ids if valid_evidence[e] and
                        evidence[e]["kind"] in allowed[kind] and evidence[e]["verdict"] == "pass"]
            return selected, set().union(*(set(e["subject_hashes"]) for e in selected)) if selected else set()

        for rid, req in requirements.items():
            sids = subject_ids(req, "requirement " + rid)
            need(req.get("kind") in KINDS and type(req.get("blocking")) is bool, "Invalid requirement kind/blocking")
            state = req.get("status")
            need(state in {"pending", "pass", "fail", "not_applicable", "deferred"}, "Invalid requirement.status")
            text(req.get("criterion"), "requirement.criterion")
            problems = []
            ids = req.get("evidence_ids", [])
            selected, covered = usable(ids, sids, req["kind"])
            views = unique_rows(req.get("required_views", []), "required_views")
            for view in views.values():
                need(view.get("subject_id") in sids, "Required view subject outside requirement")
                for field in ("min_width", "min_height"):
                    need(type(view.get(field)) is int and view[field] > 0, "Invalid minimum view dimension")
            if state == "pass":
                if not set(sids).issubset(covered):
                    problems.append("no fresh passing " + req["kind"] + " evidence for all subjects")
                selected_ids = {e["id"] for e in selected}
                available = set().union(*(evidence_views[e] for e in selected_ids)) if selected_ids else set()
                for vid, view in views.items():
                    if not any(sid == view["subject_id"] and found == vid and w >= view["min_width"] and h >= view["min_height"]
                               for sid, found, w, h in available):
                        problems.append("missing current sufficiently large view: " + view["subject_id"] + "/" + vid)
            elif state == "not_applicable":
                text(req.get("rationale"), "not_applicable rationale")
            elif state == "deferred":
                text(req.get("rationale"), "deferred rationale")
                if req["blocking"]:
                    problems.append("a blocking criterion cannot be satisfied by deferral")
            else:
                problems.append("criterion is " + state)
            if req["blocking"]:
                blockers.extend("requirement " + rid + ": " + p for p in problems)
            else:
                advisories.extend("requirement " + rid + ": " + p for p in problems)
                if state == "deferred":
                    advisories.append("requirement " + rid + " deferred: " + req["rationale"])
            report["requirements"].append({"id": rid, "status": state, "blocking": req["blocking"], "problems": problems})

        for iid, issue in issues.items():
            sids = subject_ids(issue, "issue " + iid)
            text(issue.get("description"), "issue.description")
            need(issue.get("severity") in {"blocking", "advisory"}, "Invalid issue.severity")
            need(issue.get("status") in {"open", "fixed", "deferred"}, "Invalid issue.status")
            problems = []
            if issue["status"] == "fixed":
                need(issue.get("verification_kind") in KINDS, "Fixed issue needs verification_kind")
                selected, covered = usable(issue.get("resolved_evidence_ids", []), sids, issue["verification_kind"])
                if not set(sids).issubset(covered):
                    problems.append("fixed issue has no current recheck evidence for all subjects")
            else:
                problems.append("issue remains " + issue["status"])
                if issue["status"] == "deferred":
                    text(issue.get("rationale"), "issue deferred rationale")
            target = blockers if issue["severity"] == "blocking" else advisories
            target.extend("issue " + iid + ": " + p for p in problems)

        seen = set()
        for item in preserve:
            need(isinstance(item, dict), "preserve rows must be objects")
            text(item.get("rationale"), "preserve rationale")
            p = item.get("path")
            need(p not in seen, "Duplicate preserve path")
            seen.add(p)
            failures = check_files([item], "preserve")
            blockers.extend("protected baseline: " + f for f in failures)
            report["preserved"].append({"path": p, "unchanged": not failures})
        report["schema_valid"] = True
        report["ready_to_complete"] = not blockers
        report["completion_rejected"] = task["status"] in {"ready", "complete"} and bool(blockers)
        report["task_id"] = task["id"]
        report["declared_status"] = task["status"]
    except (LedgerError, OSError, TypeError) as error:
        blockers.append("ledger invalid: " + str(error))
        report["completion_rejected"] = isinstance(data, dict) and isinstance(data.get("task"), dict) and data["task"].get("status") in {"ready", "complete"}
    report["limits"] = ["Hash validity does not prove the observation is true or the file was visually inspected.",
                        "Required criteria, source dependency closure, reviewer identity and view orientation are authored inputs.",
                        "This is a local completion check; it cannot intercept arbitrary assistant text or platform task completion."]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="Hash declared relative source/artifact paths")
    snap.add_argument("--root", required=True)
    snap.add_argument("--path", action="append", required=True)
    check = sub.add_parser("validate", help="Validate ledger and current evidence")
    check.add_argument("ledger")
    check.add_argument("--root", required=True)
    check.add_argument("--require-ready", action="store_true")
    check.add_argument("--output", help="Optional JSON report path; writes only this requested file")
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            result = snapshot(args.root, args.path)
        else:
            p = Path(args.ledger)
            need(p.stat().st_size <= MAX_JSON, "Ledger exceeds 2 MiB")
            result = validate(json.loads(p.read_text(encoding="utf-8-sig")), args.root)
        encoded = json.dumps(result, ensure_ascii=False, indent=2)
        if getattr(args, "output", None):
            Path(args.output).write_text(encoded + "\n", encoding="utf-8")
        print(encoded)
        if args.command == "validate":
            if not result["schema_valid"] or result["completion_rejected"]:
                return 1
            if args.require_ready and not result["ready_to_complete"]:
                return 2
        return 0
    except (LedgerError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
