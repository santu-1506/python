"""
Intent detection.

This is intentionally simple (keyword scoring, no ML), but it's split out
from the bot class so it can be unit tested on its own and swapped out
later (e.g. for a small classifier) without touching Chatbot.
"""

import re

INTENT_KEYWORDS = {
    "greeting": {"hi", "hello", "hey", "yo", "sup"},
    "farewell": {"bye", "goodbye", "quit", "exit", "later"},
    "thanks": {"thanks", "thank", "thx"},
    "bored": {"bored", "boring", "nothing", "idle", "dull"},
    "mood_bad": {"sad", "tired", "angry", "upset", "lonely", "stressed", "bad"},
    "mood_good": {"happy", "great", "good", "excited", "fun", "awesome", "nice"},
    "identity": {"who", "what", "name", "bot", "chatbot"},
}

# Words that flip the meaning of whatever comes right after them.
# Naive, but it kills the most annoying false positive: "not bored"
# scoring as "bored".
NEGATIONS = {"not", "no", "never", "n't", "isnt", "isn't", "dont", "don't"}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def detect_intent(text: str) -> str | None:
    """
    Returns the best-matching intent name, or None if nothing scores above
    zero. Words immediately preceded by a negation are dropped before
    scoring, so "not bored" and "I'm not happy" don't misfire.
    """
    tokens = tokenize(text)
    kept_words = set()
    for i, word in enumerate(tokens):
        preceded_by_negation = i > 0 and tokens[i - 1] in NEGATIONS
        if not preceded_by_negation:
            kept_words.add(word)

    scores = {
        intent: len(kept_words & keywords)
        for intent, keywords in INTENT_KEYWORDS.items()
    }

    best_intent, best_score = max(scores.items(), key=lambda item: item[1])
    return best_intent if best_score else None
