"""Audit the naming and package structure of read-only daily study notes."""

import argparse
from datetime import date
import json
from pathlib import Path
import re

DATE_NAME = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
HOUR_NAME = re.compile(r"([01]\d|2[0-3])-00\.md\Z")
PACKAGE = re.compile(r"^## Paket (\d+)\s+[—-]\s+\S", re.MULTILINE)


def audit(root):
    daily = Path(root) / "daily"
    if not daily.is_dir():
        raise ValueError("daily directory is missing")
    problems = []
    files = 0
    packages = 0
    days = 0
    for day_dir in sorted(daily.iterdir()):
        if day_dir.is_symlink() or not day_dir.is_dir():
            problems.append({"path": day_dir.name, "code": "unexpected_daily_entry"})
            continue
        try:
            if not DATE_NAME.fullmatch(day_dir.name):
                raise ValueError("invalid date format")
            date.fromisoformat(day_dir.name)
        except ValueError:
            problems.append({"path": day_dir.name, "code": "invalid_date_directory"})
            continue
        days += 1
        for note in sorted(day_dir.iterdir()):
            rel = f"{day_dir.name}/{note.name}"
            if note.is_symlink() or not note.is_file() or not HOUR_NAME.fullmatch(note.name):
                problems.append({"path": rel, "code": "invalid_note_filename"})
                continue
            files += 1
            content = note.read_text(encoding="utf-8")
            ids = [int(number) for number in PACKAGE.findall(content)]
            packages += len(ids)
            # The archive contains both two- and three-package notes.
            # Require numbering to start at 1 and contain no gaps or duplicates.
            if not ids or sorted(ids) != list(range(1, len(ids) + 1)):
                problems.append({"path": rel, "code": "nonsequential_package_numbers"})
            hour = note.name[:2]
            first_line = content.lstrip().splitlines()[0] if content.strip() else ""
            # Early notes used a time-only heading; newer ones include the date.
            if not (first_line.startswith(f"# {day_dir.name} {hour}:00")
                    or first_line.startswith(f"# {hour}:00")):
                problems.append({"path": rel, "code": "header_date_time_mismatch"})
    return {"days": days, "notes": files, "packages": packages,
            "problems": problems, "ok": not problems}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Audit could not run: {type(exc).__name__}\n")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['days']} days, {result['notes']} notes, {result['packages']} packages")
        for problem in result["problems"]:
            print(f"{problem['path']}: {problem['code']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
