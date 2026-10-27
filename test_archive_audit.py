import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from archive_audit import audit, main


class ArchiveAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        day = self.root / "daily" / "2026-09-23"
        day.mkdir(parents=True)
        self.note = day / "11-00.md"
        self.note.write_text("# 2026-09-23 11:00 — Study\n\n"
                             "## Paket 1 — First\n\n## Paket 2 — Second\n", encoding="utf-8")

    def test_valid_archive(self):
        report = audit(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual((report["days"], report["notes"], report["packages"]), (1, 1, 2))

    def test_missing_package_headings(self):
        self.note.write_text("# 2026-09-23 11:00\nNo packages\n", encoding="utf-8")
        self.assertEqual(audit(self.root)["problems"][0]["code"], "nonsequential_package_numbers")

    def test_duplicate_number(self):
        self.note.write_text("# 2026-09-23 11:00\n## Paket 1 — First\n## Paket 1 — Second\n", encoding="utf-8")
        self.assertFalse(audit(self.root)["ok"])

    def test_gap_in_numbering(self):
        self.note.write_text("# 2026-09-23 11:00\n## Paket 1 — First\n## Paket 3 — Third\n", encoding="utf-8")
        self.assertFalse(audit(self.root)["ok"])

    def test_legacy_three_packages_and_time_only_heading(self):
        self.note.write_text("# 11:00 — Study\n## Paket 1 — First\n## Paket 2 — Second\n"
                             "## Paket 3 — Third\n", encoding="utf-8")
        self.assertTrue(audit(self.root)["ok"])

    def test_header_mismatch(self):
        self.note.write_text("# 2026-09-23 10:00\n## Paket 1 — First\n## Paket 2 — Second\n", encoding="utf-8")
        self.assertEqual(audit(self.root)["problems"][0]["code"], "header_date_time_mismatch")

    def test_invalid_date_and_filename(self):
        (self.root / "daily" / "2026-02-30").mkdir()
        (self.note.parent / "25-00.md").write_text("bad", encoding="utf-8")
        codes = {p["code"] for p in audit(self.root)["problems"]}
        self.assertIn("invalid_date_directory", codes)
        self.assertIn("invalid_note_filename", codes)

    def test_missing_directory(self):
        with self.assertRaises(ValueError):
            audit(self.root / "absent")

    def test_cli_json_exit_status(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(["--root", str(self.root), "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["packages"], 2)
        self.note.unlink()
        (self.note.parent / "25-00.md").write_text("bad", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--root", str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
