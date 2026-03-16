from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# --- check_guess tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_guess_one_above_secret():
    # Edge case: guess is exactly one above the secret
    assert check_guess(51, 50) == "Too High"

def test_guess_one_below_secret():
    # Edge case: guess is exactly one below the secret
    assert check_guess(49, 50) == "Too Low"

def test_guess_is_1_secret_is_100():
    # FIX verification: before the fix, inverted hints would say "Go LOWER" here
    assert check_guess(1, 100) == "Too Low"

def test_guess_is_100_secret_is_1():
    # FIX verification: before the fix, inverted hints would say "Go HIGHER" here
    assert check_guess(100, 1) == "Too High"

# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_decimal_rounds_down():
    # Decimals should be truncated to int (e.g. "7.9" -> 7)
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."

def test_parse_negative_number():
    # Negative numbers should parse successfully
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_range_is_harder_than_normal():
    # FIX verification: Hard was (1,50) which is easier than Normal (1,100)
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

# --- update_score tests ---

def test_win_on_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 90  # 100 - 10*1

def test_win_score_floor():
    # After many attempts the score bonus should not go below 10
    score = update_score(0, "Win", 100)
    assert score == 10

def test_wrong_guess_subtracts_points():
    score = update_score(50, "Too High", 1)
    assert score == 45

def test_wrong_low_guess_subtracts_points():
    score = update_score(50, "Too Low", 1)
    assert score == 45
