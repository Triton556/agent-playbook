"""Local required-field checks; not complete YAML or model-quality validation."""
import re
import sys
from pathlib import Path

if __package__:
    from .utils import parse_skill_md
else:
    from utils import parse_skill_md


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    try:
        name, description, content = parse_skill_md(skill_path)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            return False, "name must be lowercase kebab-case, at most 64 characters"
        if name != skill_path.name:
            return False, "name must match the skill directory"
        if not description or len(description) > 1024 or "<" in description or ">" in description:
            return False, "description must be nonempty, at most 1024 characters, without angle brackets"
        header = content.split("---", 2)[1]
        for field in ("name", "description"):
            if sum(line.startswith(field + ":") for line in header.splitlines()) != 1:
                return False, f"exactly one {field} field is required"
        return True, "Local required-field checks passed; not full YAML or model-quality validation"
    except (OSError, UnicodeError, ValueError, IndexError) as exc:
        return False, f"Required-field check failed: {exc}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill-directory>")
        sys.exit(2)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
