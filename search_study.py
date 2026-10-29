"""Search checked-in daily study package titles and optionally their contents."""

import argparse
from datetime import date
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "daily"
PACKAGE = re.compile(r"(?m)^## Paket\s+\d+\s*[—:-]\s*(.+?)\s*$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
HOUR = re.compile(r"\d{2}-00\.md\Z")


def normalized(value: str) -> str:
    """Case-insensitive Turkish matching, including dotted/dotless I."""
    return unicodedata.normalize("NFC", value).replace("İ", "i").replace("I", "ı").casefold()


def search_packages(root: Path, query: str, limit: int = 20, full_text: bool = False,
                    since: date | None = None, until: date | None = None) -> list[dict[str, str]]:
    if not query.strip():
        raise ValueError("Search query cannot be empty")
    if limit < 1:
        raise ValueError("Limit must be positive")
    if since and until and since > until:
        raise ValueError("--since must not be after --until")
    needle = normalized(query.strip())
    results = []
    for path in sorted(root.glob("*/*.md"), reverse=True):
        if not DATE.fullmatch(path.parent.name) or not HOUR.fullmatch(path.name):
            continue
        if since or until:
            try:
                day = date.fromisoformat(path.parent.name)
            except ValueError:
                continue
            if (since and day < since) or (until and day > until):
                continue
        content = path.read_text(encoding="utf-8")
        matches = list(PACKAGE.finditer(content))
        for index, match in enumerate(matches):
            title = match.group(1).strip()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            haystack = content[match.start():end] if full_text else title
            if needle in normalized(haystack):
                results.append({"date": path.parent.name, "time": path.stem.replace("-", ":"), "title": title, "path": path.relative_to(root.parent).as_posix()})
                if len(results) >= limit:
                    return results
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the daily interview study archive offline")
    parser.add_argument("query", help="Word or phrase to find")
    parser.add_argument("--root", type=Path, default=ROOT, help="Daily archive directory")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--full-text", action="store_true", help="Search package bodies as well as titles")
    parser.add_argument("--since", type=date.fromisoformat, help="Inclusive start date (YYYY-MM-DD)")
    parser.add_argument("--until", type=date.fromisoformat, help="Inclusive end date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Print JSON results")
    args = parser.parse_args(argv)
    try:
        results = search_packages(args.root, args.query, args.limit, args.full_text, args.since, args.until)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['date']} {item['time']} | {item['title']} | {item['path']}")
        if not results:
            print("No matching packages found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
