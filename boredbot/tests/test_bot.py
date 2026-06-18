import tempfile
from pathlib import Path

import pytest

from boredbot.bot import Chatbot
from boredbot.memory import Memory


@pytest.fixture
def bot():
    with tempfile.TemporaryDirectory() as tmp:
        yield Chatbot(memory=Memory(db_path=Path(tmp) / "test.db"))


def test_empty_input_handled(bot):
    assert "Say anything" in bot.respond("   ")


def test_remembers_name(bot):
    reply = bot.respond("my name is Santu")
    assert "Santu" in reply
    assert bot.user_name == "Santu"


def test_recalls_name_after_telling_it(bot):
    bot.respond("I'm Santu")
    reply = bot.respond("what is my name")
    assert "Santu" in reply


def test_name_persists_via_memory(bot):
    bot.respond("my name is Santu")
    # simulate a fresh process reusing the same memory file
    reloaded_bot = Chatbot(memory=bot.memory)
    assert reloaded_bot.user_name == "Santu"


def test_joke_command(bot):
    from boredbot import content
    assert bot.respond("tell me a joke") in content.JOKES


def test_learn_and_recall(bot):
    bot.respond("learn good morning => rise and shine")
    reply = bot.respond("good morning")
    assert reply == "rise and shine"


def test_learn_bad_format_gives_hint(bot):
    reply = bot.respond("learn this is broken")
    assert "format" in reply.lower()


def test_game_flow_start_and_guess(bot):
    bot.respond("game")
    assert bot.active_game is not None
    bot.active_game.secret_number = 7
    reply = bot.respond("7")
    assert "Correct" in reply
    assert bot.active_game is None


def test_negation_does_not_trigger_bored_response(bot):
    from boredbot import content
    reply = bot.respond("I am not bored")
    # should NOT be one of the canned "bored" responses
    assert reply not in content.RESPONSES["bored"]


def test_help_command_lists_commands(bot):
    reply = bot.respond("help")
    assert "joke" in reply and "game" in reply
