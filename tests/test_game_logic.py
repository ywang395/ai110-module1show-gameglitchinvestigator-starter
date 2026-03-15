import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ── check_guess ──────────────────────────────────────────────────────────────

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high_returns_go_lower():
    # Bug fix: was returning "Go HIGHER!" when guess was too high
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low_returns_go_higher():
    # Bug fix: was returning "Go LOWER!" when guess was too low
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_guess_one_below_secret():
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_guess_one_above_secret():
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_string_secret_win():
    # Even-attempt glitch: secret gets converted to string
    outcome, _ = check_guess(50, "50")
    assert outcome == "Win"

def test_string_secret_single_digit_vs_two_digit():
    # Bug: string comparison "9" > "10" is True (lexicographic), causing wrong hint
    # guess=9, secret="10" → numerically too low, but string compare says too high
    # This test documents the known glitch on even attempts
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too High"  # wrong answer due to string comparison glitch


# ── get_range_for_difficulty ──────────────────────────────────────────────────

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_unknown_difficulty_defaults_to_normal():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# ── parse_guess ───────────────────────────────────────────────────────────────

def test_parse_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_non_number_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_decimal_truncates_to_int():
    # "3.7" should parse as 3, not raise an error
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


# ── update_score ──────────────────────────────────────────────────────────────

def test_win_on_first_attempt():
    # points = 100 - 10 * (1 + 1) = 80
    score = update_score(0, "Win", 1)
    assert score == 80

def test_win_minimum_score_is_10():
    # Late win should never give less than 10 points
    score = update_score(0, "Win", 100)
    assert score == 10

def test_too_high_on_even_attempt_adds_points():
    # Even attempt number → +5 for Too High
    score = update_score(50, "Too High", 2)
    assert score == 55

def test_too_high_on_odd_attempt_deducts_points():
    # Odd attempt number → -5 for Too High
    score = update_score(50, "Too High", 3)
    assert score == 45

def test_too_low_always_deducts_points():
    score = update_score(50, "Too Low", 1)
    assert score == 45

def test_unknown_outcome_keeps_score():
    score = update_score(50, "Draw", 1)
    assert score == 50
