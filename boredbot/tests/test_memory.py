import tempfile
from pathlib import Path

import pytest

from boredbot.memory import Memory


@pytest.fixture
def memory():
    with tempfile.TemporaryDirectory() as tmp:
        yield Memory(db_path=Path(tmp) / "test.db")


def test_profile_set_and_get(memory):
    memory.set_profile("user_name", "Santu")
    assert memory.get_profile("user_name") == "Santu"


def test_profile_missing_key_returns_none(memory):
    assert memory.get_profile("nonexistent") is None


def test_profile_overwrite(memory):
    memory.set_profile("user_name", "Santu")
    memory.set_profile("user_name", "Venkat")
    assert memory.get_profile("user_name") == "Venkat"


def test_learned_response_round_trip(memory):
    memory.add_learned_response("good morning", "rise and grind")
    all_responses = memory.all_learned_responses()
    assert all_responses["good morning"] == "rise and grind"


def test_learned_response_is_case_normalized(memory):
    memory.add_learned_response("HELLO THERE", "hi back")
    assert "hello there" in memory.all_learned_responses()


def test_delete_learned_response(memory):
    memory.add_learned_response("foo", "bar")
    assert memory.delete_learned_response("foo") is True
    assert "foo" not in memory.all_learned_responses()


def test_delete_nonexistent_returns_false(memory):
    assert memory.delete_learned_response("nope") is False


def test_persists_across_instances():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        Memory(db_path=db_path).set_profile("user_name", "Santu")
        # new instance, same file, simulates a restart
        reloaded = Memory(db_path=db_path)
        assert reloaded.get_profile("user_name") == "Santu"
