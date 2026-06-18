"""Guess-the-number game, now self-contained instead of bolted onto Chatbot."""

import random
import re

from .base import Game

STOP_PHRASES = {"stop", "quit game", "end game"}


class GuessNumberGame(Game):
    name = "guess_number"

    def __init__(self, low: int = 1, high: int = 10):
        self.low = low
        self.high = high
        self.secret_number = random.randint(low, high)
        self._finished = False

    def start(self) -> str:
        return (
            f"Tiny game: I am thinking of a number from {self.low} to {self.high}. "
            "Send a number and I will tell you if it is high, low, or correct. "
            "Type 'stop' to quit anytime."
        )

    def handle_input(self, text: str) -> str | None:
        lowered = text.lower().strip()

        if lowered in STOP_PHRASES:
            self._finished = True
            return "Game stopped. We can pretend you were about to win."

        match = re.search(r"\b(\d+)\b", text)
        if not match:
            return None  # not a guess, let the bot handle it normally

        guess = int(match.group(1))
        if guess == self.secret_number:
            self._finished = True
            return "Correct. Suspiciously competent guessing."
        if guess < self.secret_number:
            return "Too low. Try a bigger number."
        return "Too high. Try a smaller number."

    @property
    def is_finished(self) -> bool:
        return self._finished
