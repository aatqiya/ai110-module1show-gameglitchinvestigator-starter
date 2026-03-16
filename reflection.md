# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

---

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface — the UI loaded, I could type a guess and hit Submit — but it was impossible to actually win. I identified at least three concrete bugs right away by playing and using the Developer Debug Info tab.

**Bug 1 — Inverted hints:** Every time I guessed, the hint was backwards. If I guessed 70 and the secret was 50, the game told me "Go HIGHER!" instead of "Go LOWER!". I verified this by opening the debug tab to see the secret number, then guessing a number I knew was higher and watching the wrong hint appear.

**Bug 2 — Alternating int/str secret conversion:** On every even-numbered attempt (2nd, 4th, 6th…), the secret number was silently converted to a string before being compared to my integer guess. This caused the comparison logic to break completely — Python string ordering means `"5" > "40"` is `True` because `"5"` > `"4"` alphabetically. So even if I guessed the exact correct number on an even attempt, the outcome could still be wrong.

**Bug 3 — Hard difficulty was easier than Normal:** The Hard difficulty used a range of 1–50, which is actually a smaller and easier range than Normal's 1–100. This is the opposite of what the label says and would confuse any player who thought they were being challenged.

**Bonus Bug — `attempts` counter started at 1:** The session state initialized `attempts = 1` instead of `0`. This meant the "Attempts left" display was always one lower than the real remaining attempts, and the first guess was labeled internally as attempt #2.

---

## 2. How did you use AI as a teammate?

I used **Claude Code** (Anthropic's CLI AI coding assistant) as my primary AI collaborator throughout this project. I also referenced ChatGPT to understand Streamlit's session state model (how reruns work and why variables reset).

**Correct AI suggestion:** When I asked Claude Code to explain why hints were wrong, it immediately identified the inverted comparison messages in `check_guess` — `if guess > secret: return "Too High", "📈 Go HIGHER!"` — and explained that the message said "Go HIGHER" when the player should actually go lower. I verified this fix by running `pytest` and confirming `test_guess_too_high` passed, then playing the game manually with the debug tab open to confirm the hint now correctly said "Go LOWER!" when I guessed above the secret.

**Incorrect or misleading AI suggestion:** At first, Claude Code kept the `update_score` function with the original confusing logic that added +5 points to "Too High" guesses on even-numbered attempts. This was technically "moved" correctly during the refactor but the logic itself is still arbitrary and unfair — it rewards wrong guesses on even turns for no clear reason. I had to explicitly ask it to simplify this to a flat -5 for any wrong guess, which is more predictable and testable. The lesson: AI will faithfully copy bad logic unless you point it out.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only when two things were true: the automated `pytest` suite passed, and I could confirm the correct behavior by playing the game manually with the Developer Debug Info tab open. I didn't trust one without the other — a test can pass while the UI still behaves wrong if the wiring in app.py is off.

**Pytest run for the inverted hint fix:** I ran `python3 -m pytest tests/ -v` and watched `test_guess_too_high` — which calls `check_guess(60, 50)` and asserts the result is `"Too High"` — pass cleanly. Before the fix, this test would have either failed (wrong return) or crashed (TypeError from the int/str alternation). Seeing it go green confirmed the core logic was sound.

**Manual test for the int/str alternation bug:** I played the game, opened the debug tab, noted the secret was (for example) 42, then deliberately made two wrong guesses so I was on attempt #2 (an even attempt). I then guessed 42 exactly. Before the fix, the game would not register a win because the secret was cast to `"42"` (string) and the comparison broke. After the fix, it correctly returned "Win".

**AI-assisted test design:** I asked Claude Code to help design edge-case tests — for instance, verifying that `parse_guess` correctly handles decimal input like `"7.9"` (should parse as `7`), empty strings (should return an error), and non-numeric text like `"abc"` (should return an error). Having these tests gave me confidence that the parsing logic was robust beyond the happy path.

---

## 4. What did you learn about Streamlit and state?

Streamlit works differently from most Python programs: every time the user interacts with the app (clicks a button, changes a dropdown), the entire Python script re-runs from top to bottom. This means any variable you define normally — like `secret = random.randint(1, 100)` — gets a brand new value every single run, which is why the secret number kept changing.

The fix is `st.session_state`, which is a dictionary that Streamlit keeps alive across reruns. By checking `if "secret" not in st.session_state` before generating a new number, the secret is only created once at the very first run and then preserved. I'd explain it to a friend this way: imagine every button click hits "Refresh" on the whole page, but `session_state` is like a sticky note on the side of the screen that survives every refresh.

---

## 5. Looking ahead: your developer habits

**Habit I want to reuse:** Reading code with the debug tab open while playing. Being able to see the actual secret number, attempt count, and history in real time made the bugs obvious in seconds rather than minutes of guessing. In future projects, I want to always build a "debug panel" early — even a simple `st.write(vars)` — so I can observe state directly instead of reasoning about it in my head.

**What I'd do differently:** Next time I use AI to generate or move code, I'll ask it to also explain *why* each line exists, not just what it does. The `update_score` function had a nonsensical "add 5 points on even-attempt wrong guesses" rule that AI moved faithfully without questioning. If I had asked "does this scoring logic make sense?" up front, I'd have caught it earlier.

**How this project changed my view of AI-generated code:** I used to think AI-generated code was either right or wrong and you'd know quickly which. This project showed me a third category: code that *looks* reasonable and *almost* works, but contains subtle logic bugs (like alternating type casting) that only surface under specific conditions. AI is a fast first draft, but it needs a human to verify the behavior in context — not just read the syntax.
