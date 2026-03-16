def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard was (1,50) which is easier than Normal (1,100). Corrected to (1,200).
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Refactored from app.py using Copilot Agent mode
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    # FIX: Original hints were inverted — "Go HIGHER!" was shown when guess was
    # too high. Fixed so Too High -> Go LOWER, Too Low -> Go HIGHER.
    # FIX: Removed alternating int/str secret conversion that caused wrong comparisons.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # Refactored from app.py. Simplified scoring: win gives points, wrong guess costs 5.
    if outcome == "Win":
        points = max(100 - 10 * attempt_number, 10)
        return current_score + points
    return current_score - 5
