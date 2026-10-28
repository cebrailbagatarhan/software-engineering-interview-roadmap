"""Pick interview practice questions from the checked-in high-yield bank."""

import argparse
import random
import re
from pathlib import Path

BANK = Path(__file__).resolve().parent / "questions/high-yield/01-foundations-networking-backend.md"
QUESTION = re.compile(r"(?m)^###\s+(\d+)\.\s+(.+?)\s*$")


def load_questions(path: Path = BANK) -> list[tuple[int, str, str]]:
    """Return numbered questions with their optional coaching notes."""
    source = path.read_text(encoding="utf-8")
    matches = list(QUESTION.finditer(source))
    questions = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        notes = source[match.end():end]
        notes = re.split(r"(?m)^(?:---|#{1,3}\s)", notes, maxsplit=1)[0].strip()
        questions.append((int(match.group(1)), match.group(2).strip(), notes))
    return questions


def select_questions(questions: list[tuple[int, str, str]], count: int, seed: int | None = None) -> list[tuple[int, str, str]]:
    if count < 1 or count > len(questions):
        raise ValueError(f"Question count must be between 1 and {len(questions)}")
    return random.Random(seed).sample(questions, count)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Practice random interview questions offline")
    parser.add_argument("--count", type=int, default=5, help="Number of questions (default: 5)")
    parser.add_argument("--seed", type=int, help="Repeatable selection seed")
    parser.add_argument("--exclude", default="", help="Comma-separated question numbers to skip (e.g. 1,2,5)")
    parser.add_argument("--show-notes", action="store_true", help="Show coaching notes/expected answers")
    args = parser.parse_args(argv)
    try:
        bank = load_questions()
        excluded = set()
        if args.exclude:
            parts = [part.strip() for part in args.exclude.split(",")]
            if not all(re.fullmatch(r"[0-9]+", part) for part in parts):
                raise ValueError("--exclude requires comma-separated question numbers")
            excluded = {int(part) for part in parts}
            unknown = excluded - {number for number, _, _ in bank}
            if unknown:
                raise ValueError(f"Unknown question numbers: {', '.join(map(str, sorted(unknown)))}")
        eligible = [question for question in bank if question[0] not in excluded]
        questions = select_questions(eligible, args.count, args.seed)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    for number, title, notes in questions:
        print(f"\n{number}. {title}")
        if args.show_notes and notes:
            print(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
