import contextlib
from datetime import date
import io
import json
from pathlib import Path
import tempfile
import unittest

from study_summary import main, summarize


class StudySummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def note(self, day, filename, text):
        folder = self.root / day
        folder.mkdir(exist_ok=True)
        (folder / filename).write_text(text, encoding="utf-8")

    def test_counts_notes_and_packages_per_day(self):
        self.note("2026-09-14", "10-00.md", "## Paket 1 — A\n## Paket 2 — B\n")
        self.note("2026-09-14", "11-00.md", "## Paket 1 — C\n")
        self.note("2026-09-15", "00-00.md", "## Paket 1 - D\n")
        report = summarize(self.root)
        self.assertEqual(report["totals"], {"days": 2, "notes": 3, "packages": 4})
        self.assertEqual(report["days"][0]["packages"], 3)

    def test_date_filters_are_inclusive(self):
        self.note("2026-09-14", "00-00.md", "## Paket 1 — A\n")
        self.note("2026-09-15", "00-00.md", "## Paket 1 — B\n")
        report = summarize(self.root, date(2026, 9, 15), date(2026, 9, 15))
        self.assertEqual(report["days"][0]["date"], "2026-09-15")
        self.assertEqual(report["totals"]["notes"], 1)

    def test_ignores_non_archive_paths_and_invalid_hours(self):
        self.note("2026-09-14", "24-00.md", "## Paket 1 — A\n")
        self.note("not-a-date", "10-00.md", "## Paket 1 — B\n")
        self.note("2026-09-14", "10-30.md", "## Paket 1 — C\n")
        self.assertEqual(summarize(self.root)["totals"]["notes"], 0)

    def test_empty_note_is_counted_without_packages(self):
        self.note("2026-09-14", "10-00.md", "# No packages\n")
        self.assertEqual(summarize(self.root)["totals"], {"days": 1, "notes": 1, "packages": 0})

    def test_empty_archive(self):
        self.assertEqual(summarize(self.root)["totals"], {"days": 0, "notes": 0, "packages": 0})

    def test_invalid_date_range(self):
        with self.assertRaisesRegex(ValueError, "since"):
            summarize(self.root, date(2026, 9, 16), date(2026, 9, 15))

    def test_missing_directory(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            summarize(self.root / "missing")

    def test_cli_json_output(self):
        self.note("2026-09-14", "10-00.md", "## Paket 1 — A\n")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root), "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["totals"]["packages"], 1)


if __name__ == "__main__":
    unittest.main()
