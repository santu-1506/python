"""
Core Chatbot class.

This file is intentionally small. Its only job is to coordinate:
  - intents.py for understanding what the user means
  - content.py for canned replies
  - games/ for anything stateful and turn-based
  - memory.py for anything that needs to survive a restart

If you find yourself adding a big chunk of new logic directly into this
file, it probably belongs in one of those modules instead.
"""

import difflib
import logging
import random
import re
from datetime import datetime

from . import content
from .games import AVAILABLE_GAMES, Game
from .intents import detect_intent
from .memory import Memory

logger = logging.getLogger(__name__)

NAME_PATTERNS = [
    re.compile(r"\bmy name is ([a-zA-Z][a-zA-Z ]{1,30})", re.IGNORECASE),
    re.compile(r"\bi am ([a-zA-Z][a-zA-Z ]{1,30})", re.IGNORECASE),
    re.compile(r"\bi'm ([a-zA-Z][a-zA-Z ]{1,30})", re.IGNORECASE),
]

LEARN_PATTERN = re.compile(r"learn\s+(.+?)\s*=>\s*(.+)", re.IGNORECASE)

STOPWORDS = {"about", "because", "really", "think"}


class Chatbot:
    def __init__(self, memory: Memory | None = None):
        self.memory = memory or Memory()
        self.user_name: str | None = self.memory.get_profile("user_name")
        self.last_topic: str | None = None
        self.active_game: Game | None = None

    # ---- learning new trigger -> response pairs ----

    def learn(self, text: str) -> str:
        match = LEARN_PATTERN.match(text)
        if not match:
            return "Use this format: learn trigger phrase => response I should say"

        trigger, response = match.groups()
        trigger = trigger.strip()
        self.memory.add_learned_response(trigger, response.strip())
        logger.info("Learned new trigger: %r", trigger)
        return f"Learned. If you say something like '{trigger}', I will remember that."

    def learned_reply(self, text: str) -> str | None:
        learned = self.memory.all_learned_responses()
        if not learned:
            return None

        match = difflib.get_close_matches(text.lower(), list(learned), n=1, cutoff=0.68)
        return learned[match[0]] if match else None

    # ---- remembering the user's name ----

    def maybe_remember_name(self, text: str) -> str | None:
        for pattern in NAME_PATTERNS:
            match = pattern.search(text)
            if match:
                self.user_name = match.group(1).strip().title()
                self.memory.set_profile("user_name", self.user_name)
                logger.info("Stored user name: %s", self.user_name)
                return f"Nice to meet you, {self.user_name}."
        return None

    # ---- fallback when nothing else matches ----

    def prompt_for_topic(self, text: str) -> str:
        words = [
            word for word in re.findall(r"[a-z']+", text.lower())
            if len(word) > 4 and word not in STOPWORDS
        ]
        if words:
            self.last_topic = random.choice(words)
            return (
                f"Tell me more about {self.last_topic}. "
                "Is it interesting, annoying, or just taking up brain space?"
            )
        return "I can work with that. Give me one more detail."

    # ---- games ----

    def start_game(self, name: str = "guess_number") -> str:
        game_cls = AVAILABLE_GAMES.get(name)
        if not game_cls:
            return f"I do not know a game called '{name}'."
        self.active_game = game_cls()
        return self.active_game.start()

    # ---- main entry point ----

    def respond(self, text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            return "Say anything. Even keyboard smashing gives us a place to start."

        if self.active_game is not None:
            reply = self.active_game.handle_input(cleaned)
            if reply is not None:
                if self.active_game.is_finished:
                    self.active_game = None
                return reply
            # reply was None: input wasn't for the game, fall through

        lowered = cleaned.lower()

        if lowered in {"help", "commands"}:
            return (
                "Commands: joke, question, challenge, story, time, name, "
                "game, learn trigger => response, quit"
            )

        if lowered.startswith("learn "):
            return self.learn(cleaned)

        remembered_name = self.maybe_remember_name(cleaned)
        if remembered_name:
            return remembered_name

        learned = self.learned_reply(cleaned)
        if learned:
            return learned

        if "joke" in lowered:
            return random.choice(content.JOKES)
        if "question" in lowered:
            return random.choice(content.QUESTIONS)
        if "challenge" in lowered:
            return random.choice(content.CHALLENGES)
        if "story" in lowered:
            return random.choice(content.STORY_STARTERS)
        if "time" in lowered:
            return f"It is {datetime.now().strftime('%I:%M %p')}."
        if "name" in lowered and self.user_name:
            return f"You told me your name is {self.user_name}."
        if "game" in lowered:
            return self.start_game()

        intent = detect_intent(cleaned)
        if intent:
            return random.choice(content.RESPONSES[intent])

        return self.prompt_for_topic(cleaned)
