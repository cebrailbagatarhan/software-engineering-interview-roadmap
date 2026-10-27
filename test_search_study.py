"""Tests for offline daily study archive search."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from search_study import main, search_packages


class StudySearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "daily"
        older = self.root / "2026-09-22"
        older.mkdir(parents=True)
        (older / "10-00.md").write_text("## Paket 1 — Veritabanı indeksleri\n### İçerik\nB+Tree\n", encoding="utf-8")
        newer = self.root / "2026-09-23"
        newer.mkdir(parents=True)
        (newer / "11-00.md").write_text("## Paket 1 — İşletim Sistemi\n### İçerik\nfsync ve disk\n\n## Paket 2 — Ağlar\n### İçerik\nTCP\n", encoding="utf-8")
        (newer / "notes.md").write_text("## Paket 1 — Veritabanı\n", encoding="utf-8")

    def test_turkish_title_and_date_order(self):
        self.assertEqual([x["title"] for x in search_packages(self.root, "İŞLETİM")], ["İşletim Sistemi"])
        self.assertEqual(search_packages(self.root, "indeks")[0]["path"], "daily/2026-09-22/10-00.md")

    def test_full_text_opt_in(self):
        self.assertEqual(search_packages(self.root, "fsync"), [])
        self.assertEqual(search_packages(self.root, "fsync", full_text=True)[0]["title"], "İşletim Sistemi")

    def test_limit_and_invalid_files(self):
        self.assertEqual(len(search_packages(self.root, "a", limit=1)), 1)
        self.assertEqual(search_packages(self.root, "Veritabanı", full_text=False)[0]["date"], "2026-09-22")

    def test_empty_query_and_limit_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            search_packages(self.root, " ")
        with self.assertRaisesRegex(ValueError, "positive"):
            search_packages(self.root, "a", limit=0)

    def test_json_cli(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["İşletim", "--root", str(self.root), "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())[0]["time"], "11:00")


if __name__ == "__main__":
    unittest.main()
