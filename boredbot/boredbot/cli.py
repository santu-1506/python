"""
Command-line entry point.

Run with `boredbot` (after install) or `python -m boredbot.cli`.
"""

import argparse
import logging
import random
from pathlib import Path

from . import content
from .bot import Chatbot
from .memory import Memory

BOT_NAME = "BoredBot"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boredbot",
        description="A small terminal chatbot for fighting boredom.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Path to the SQLite memory file (default: data/memory.db).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose logging.",
    )
    return parser


def configure_logging(debug: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def run(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.debug)

    memory = Memory(db_path=args.db) if args.db else Memory()
    bot = Chatbot(memory=memory)

    greeting = f"Hey, I am {BOT_NAME}. Type 'help' for commands or 'quit' to leave."
    if bot.user_name:
        greeting = f"Hey {bot.user_name}, welcome back. Type 'help' for commands."
    print(f"{BOT_NAME}: {greeting}")

    while True:
        try:
            user_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{BOT_NAME}: Bye.")
            break

        if user_text.strip().lower() in {"quit", "exit", "bye"}:
            print(f"{BOT_NAME}: {random.choice(content.RESPONSES['farewell'])}")
            break

        print(f"{BOT_NAME}: {bot.respond(user_text)}")


if __name__ == "__main__":
    run()
