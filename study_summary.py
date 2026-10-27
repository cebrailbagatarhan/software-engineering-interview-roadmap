"""Read-only daily study archive workload summary.

Usage: python study_summary.py --json --since 2026-09-20
"""

import argparse
from datetime import date
import json
from pathlib import Path
import re

NOTE_NAME = re.compile(r"^(\d{2})-00\.md$")
PACKAGE_HEADING = re.compile(r"^##\s+Paket\s+\d+\s+[—–-]\s+", re.MULTILINE)


def summarize(root: Path, since: date | None = None, until: date | None = None) -> dict:
    """Count checked-in notes and package headings, grouped by calendar day."""
    if not root.is_dir():
        raise ValueError(f"Archive directory does not exist: {root}")
    if since and until and since > until:
        raise ValueError("--since must not be after --until")

    by_day = {}
    for path in sorted(root.glob("*/*.md")):
        try:
            day = date.fromisoformat(path.parent.name)
        except ValueError:
            continue
        match = NOTE_NAME.fullmatch(path.name)
        if not match or int(match.group(1)) > 23:
            continue
        if (since and day < since) or (until and day > until):
            continue
        counts = by_day.setdefault(day.isoformat(), {"date": day.isoformat(), "notes": 0, "packages": 0})
        counts["notes"] += 1
        counts["packages"] += len(PACKAGE_HEADING.findall(path.read_text(encoding="utf-8")))

    days = [by_day[key] for key in sorted(by_day)]
    return {"days": days, "totals": {
        "days": len(days),
        "notes": sum(row["notes"] for row in days),
        "packages": sum(row["packages"] for row in days),
    }}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent / "daily")
    parser.add_argument("--since", type=date.fromisoformat, help="Inclusive YYYY-MM-DD")
    parser.add_argument("--until", type=date.fromisoformat, help="Inclusive YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        report = summarize(args.root, args.since, args.until)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for row in report["days"]:
            print(f'{row["date"]}: {row["notes"]} notes, {row["packages"]} packages')
        total = report["totals"]
        print(f'Total: {total["days"]} days, {total["notes"]} notes, {total["packages"]} packages')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
