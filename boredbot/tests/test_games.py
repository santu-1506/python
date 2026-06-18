from boredbot.games.guess_number import GuessNumberGame


def test_start_returns_intro_message():
    game = GuessNumberGame(low=1, high=10)
    intro = game.start()
    assert "1" in intro and "10" in intro


def test_correct_guess_ends_game():
    game = GuessNumberGame(low=5, high=5)  # rigged: only one possible number
    reply = game.handle_input("5")
    assert "Correct" in reply
    assert game.is_finished is True


def test_too_low_guess():
    game = GuessNumberGame(low=1, high=10)
    game.secret_number = 8
    reply = game.handle_input("2")
    assert "Too low" in reply
    assert game.is_finished is False


def test_too_high_guess():
    game = GuessNumberGame(low=1, high=10)
    game.secret_number = 2
    reply = game.handle_input("8")
    assert "Too high" in reply


def test_stop_ends_game_without_revealing():
    game = GuessNumberGame()
    reply = game.handle_input("stop")
    assert game.is_finished is True
    assert "stopped" in reply.lower()


def test_non_numeric_input_returns_none():
    game = GuessNumberGame()
    assert game.handle_input("hello") is None
