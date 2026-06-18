# BoredBot

A small terminal chatbot that fights boredom with jokes, questions, tiny
games, and writing prompts. It remembers your name and anything you
teach it across sessions (backed by SQLite).

## How to Run

1. Open a terminal and go to the project folder:

```bash
cd "/Users/venkatasantosh/Documents/python projects/boredbot"
```

2. Create and activate a virtual environment with Python 3.10 or newer:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

The version should be Python 3.10 or newer. On macOS, plain `python3`
may point to Python 3.9, which is too old for this project.

3. Start BoredBot in the terminal after the virtual environment is active:

```bash
python -m boredbot.cli
```

You can also run it directly through the virtual environment without activating it:

```bash
.venv/bin/python -m boredbot.cli
```

4. Type a command such as `help`, `joke`, `game`, or `time`.

5. Exit the bot:

```text
quit
```

Optional: install the project in editable mode if you want to run it as a command-line shortcut:

```bash
pip install -e .
boredbot
```

If the shortcut cannot import the package, use the module command from the project folder:

```bash
python -m boredbot.cli
```

Useful run options:

```bash
python -m boredbot.cli --debug          # verbose logging
python -m boredbot.cli --db ./custom.db # use a different memory file
```

## How to Run the Frontend

1. Go to the project folder and activate the virtual environment:

```bash
cd "/Users/venkatasantosh/Documents/python projects/boredbot"
source .venv/bin/activate
```

2. Install the frontend dependency:

```bash
pip install -e ".[frontend]"
```

3. Start the Streamlit app:

```bash
streamlit run streamlit_app.py
```

4. Open the local URL that Streamlit prints, usually:

```text
http://localhost:8501
```

## Commands

- `joke`, `question`, `challenge`, `story` — get a random one
- `game` — start the number-guessing game
- `time` — current time
- `my name is <name>` — bot remembers you, even after a restart
- `learn <trigger> => <response>` — teach the bot a custom reply
- `help` — list commands
- `quit` / `exit` / `bye` — leave

## Project layout

```
boredbot/
├── boredbot/
│   ├── bot.py        core Chatbot class — coordinates everything else
│   ├── intents.py    keyword-based intent detection (with negation handling)
│   ├── content.py    jokes / questions / challenges / story starters
│   ├── memory.py     SQLite persistence (name + learned responses)
│   ├── cli.py         input/output loop, argparse, logging
│   └── games/
│       ├── base.py          Game interface — implement this to add a new game
│       └── guess_number.py  the number guessing game
├── tests/             pytest suite, one file per module
└── data/              memory.db lives here at runtime (gitignored)
```

## Why it's structured this way

The original version was a single 200-line script. The split here is
meant to make each piece independently testable and easy to extend:

- **Adding a new game** means writing one file in `games/` that
  implements `Game`, then registering it in `games/__init__.py`.
  `bot.py` never needs to change.
- **Persistence is isolated** in `memory.py`. If you ever want Postgres
  instead of SQLite, that's the only file that changes.
- **Intent detection is a pure function** (`detect_intent`) with no
  dependency on the bot class, so it's trivial to unit test edge cases
  like negation ("I am *not* bored" should not trigger the "bored"
  response).

## Tests

```bash
pip install -e ".[dev]"
pytest
```

31 tests covering intents, memory persistence, game logic, and the bot's
end-to-end behavior (including that learned responses and your name
actually survive a process restart).
