"""
Game registry.

To add a new game: write a class implementing Game in its own file,
then add it to AVAILABLE_GAMES below. The bot picks games by name from
this dict, so nothing else needs to change.
"""

from .base import Game
from .guess_number import GuessNumberGame

AVAILABLE_GAMES: dict[str, type[Game]] = {
    "guess_number": GuessNumberGame,
}

__all__ = ["Game", "GuessNumberGame", "AVAILABLE_GAMES"]
