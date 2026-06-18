"""
Tiny interface every game must follow.

The goal: adding a new game (hangman, word chain, trivia, whatever)
should mean writing one new file in this folder and registering it in
games/__init__.py. Nothing in bot.py should need to change.
"""

from abc import ABC, abstractmethod


class Game(ABC):
    """Base class for all mini-games."""

    name: str = "game"

    @abstractmethod
    def start(self) -> str:
        """Called once when the game begins. Returns the intro message."""

    @abstractmethod
    def handle_input(self, text: str) -> str | None:
        """
        Called with each user message while this game is active.
        Return a string to send back to the user, or None if this input
        wasn't meant for the game (lets the bot fall through to normal
        handling instead of swallowing every message).
        """

    @property
    @abstractmethod
    def is_finished(self) -> bool:
        """True once the game has ended and should be torn down."""
