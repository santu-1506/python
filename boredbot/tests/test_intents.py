from boredbot.intents import detect_intent


def test_basic_greeting():
    assert detect_intent("hey there") == "greeting"


def test_basic_bored():
    assert detect_intent("I am so bored right now") == "bored"


def test_negation_kills_false_positive():
    # this is the bug we specifically fixed: "not bored" used to score
    # as the "bored" intent because the word overlap check ignored negation
    assert detect_intent("I am not bored") is None


def test_negation_with_contraction():
    assert detect_intent("I'm not happy today") != "mood_good"


def test_no_match_returns_none():
    assert detect_intent("xyz qwerty asdf") is None


def test_farewell():
    assert detect_intent("ok bye") == "farewell"


def test_identity_question():
    assert detect_intent("who are you") == "identity"
