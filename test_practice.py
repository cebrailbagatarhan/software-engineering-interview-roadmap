"""Offline tests for the interview practice picker."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from practice import load_questions, main, select_questions


class PracticeTests(unittest.TestCase):
    def test_checked_in_bank_has_40_unique_questions(self):
        questions = load_questions()
        self.assertEqual(len(questions), 40)
        self.assertEqual([number for number, _, _ in questions], list(range(1, 41)))
        self.assertTrue(all(title for _, title, _ in questions))

    def test_seed_is_repeatable_without_replacement(self):
        questions = load_questions()
        selected = select_questions(questions, 5, seed=42)
        self.assertEqual(selected, select_questions(questions, 5, seed=42))
        self.assertEqual(len({number for number, _, _ in selected}), 5)

    def test_default_output_hides_coaching_notes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--count", "1", "--seed", "7"]), 0)
        self.assertNotIn("**Beklenen:**", output.getvalue())
        self.assertNotIn("**Interviewer ne ölçüyor?**", output.getvalue())

    def test_notes_are_optional(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(["--count", "40", "--seed", "1", "--show-notes"])
        self.assertIn("**Beklenen:**", output.getvalue())

    def test_invalid_count_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--count", "41"])
        self.assertEqual(caught.exception.code, 2)

    def test_excluded_questions_are_not_selected_and_seed_is_repeatable(self):
        output = io.StringIO()
        args = ["--count", "37", "--seed", "42", "--exclude", "1, 2,3"]
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(args), 0)
        first = output.getvalue()
        for number in (1, 2, 3):
            self.assertNotIn(f"\\n{number}. ", first)
        self.assertEqual(len([line for line in first.splitlines() if line.strip()]), 37)
        with contextlib.redirect_stdout(io.StringIO()) as repeated:
            main(args)
        self.assertEqual(first, repeated.getvalue())

    def test_invalid_exclusions_are_rejected(self):
        for value in ("1,,2", "abc", "0", "41"):
            with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(["--count", "1", "--exclude", value])
                self.assertEqual(caught.exception.code, 2)

    def test_count_cannot_exceed_remaining_questions(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--count", "39", "--exclude", "1,2"])
        self.assertEqual(caught.exception.code, 2)

    def test_parser_handles_custom_bank(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "questions.md"
            path.write_text("### 1. First question?\n\nHint one\n\n---\n\n### 2. Second?\n\nHint two\n", encoding="utf-8")
            self.assertEqual(load_questions(path), [(1, "First question?", "Hint one"), (2, "Second?", "Hint two")])


if __name__ == "__main__":
    unittest.main()
