"""
Static content used by the bot: canned responses, jokes, questions,
challenges, and story starters.

Keeping this separate from bot.py means non-engineers (or future-you at
2am) can add new lines without touching any logic.
"""

RESPONSES = {
    "greeting": [
        "Hey. What kind of boredom are we fighting today?",
        "Hi. I am here for idle chatter, tiny games, and questionable trivia.",
        "Hello. Tell me a thought, a complaint, or just type 'bored'.",
    ],
    "farewell": [
        "Later. May your next distraction be better than scrolling.",
        "Bye. Come back when boredom gets loud again.",
        "See you. I will keep the conversation chair warm.",
    ],
    "thanks": [
        "Anytime.",
        "You are welcome.",
        "No problem. That is basically my job.",
    ],
    "bored": [
        "Let us fix that. Type 'game', 'question', 'story', 'joke', or 'challenge'.",
        "Boredom detected. I can start a tiny game, ask a weird question, or give you a challenge.",
        "Then we need a diversion. Want a quick game, a writing prompt, or a random challenge?",
    ],
    "mood_bad": [
        "That sounds rough. Want a distraction, a joke, or a low-effort challenge?",
        "I hear you. We can keep it light, or you can vent for a minute.",
        "That is not nothing. Want me to ask questions or switch to something fun?",
    ],
    "mood_good": [
        "Nice. What is making the day better?",
        "Good. We should preserve that energy. Want a game or a weird question?",
        "I like that. Give me one tiny detail from your day.",
    ],
    "identity": [
        "I am BoredBot, a small CLI chatbot built to make empty minutes less empty.",
        "I am a terminal buddy. No cloud brain, just local rules, memory, and a lot of prompts.",
    ],
}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break. It said: no problem, I will go to sleep.",
    "Debugging is like being a detective in a mystery where you are also the culprit.",
]

QUESTIONS = [
    "If your day had a movie title, what would it be?",
    "What is a tiny skill you would learn instantly if you could?",
    "Would you rather explore the ocean floor or deep space?",
    "What food is overrated, but you still respect its confidence?",
]

CHALLENGES = [
    "Name five blue things in the room in ten seconds.",
    "Write a six-word story about a missing sandwich.",
    "Stand up, stretch, and come back with one dramatic sentence.",
    "Invent a superhero whose power is only useful on Tuesdays.",
]

STORY_STARTERS = [
    "The vending machine blinked twice and whispered the wrong name.",
    "At exactly 3:14 PM, every phone in town played the same unknown song.",
    "The astronaut opened the toolbox and found a handwritten apology.",
]
