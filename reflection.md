# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
    The game look completely Normal when I first run it. It does not have any visible bug.
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
    After trying for about 2 games
    1. I noticed that the game will not start over even after you had lost. I expected that after the game is over it would start over when I press restart. Attempt would refresh. It is also expected to give new number.
    2. The hints were reverse. I expected the hints would give me higher if I guessed lower than the actaul values.
    3. The Difficulty level does change no matter which mode is set. I expected the range of random number would change if I change the difficulties level.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used Claude Code (Claude Sonnet) as my AI assistant throughout this project to help identify and fix bugs in the game.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Claude correctly identified that the hint messages in `check_guess` were reversed  "Go HIGHER!" was being returned when the guess was too high, and "Go LOWER!" when it was too low. I verified this by running the game, entering a number I knew was lower than the secret, and confirming the hint now correctly said "Go HIGHER!" after the fix.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  Claude suggested using `st.empty()` placeholders to fix the info bar and debug panel rendering order. While the idea was correct, the initial suggestion to move the debug expander to the bottom of the page was not what I wanted. I had to clarify that I wanted it to stay in its original position, and Claude then revised the approach to use a placeholder instead.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I manually tested each fix by running the Streamlit app and reproducing the exact scenario that caused the bug. For example, after fixing the game-over hint bug, I intentionally lost a game and checked whether the last hint still appeared on the screen afterward.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  I manually tested the double-submit bug by typing a guess and clicking Submit once. Before the fix, the attempt counter would deduct but the guess would not appear in history until the second click. After wrapping the input in `st.form`, a single click correctly processed the guess, updated the history, and showed the hint all at once.

- Did AI help you design or understand any tests? How?
  Yes, Claude explained that the double-submit issue was caused by Streamlit processing one widget interaction per rerun, meaning the text input value and button click were not captured together. This helped me understand what scenario to test and why the form-based fix resolved it.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  Every time the user interacted with the page, Streamlit reran the entire script from top to bottom. Without `st.session_state`, `random.randint()` would be called again on every rerun, generating a new secret number each time. The fix was to only generate the secret once and store it in `st.session_state` so it persists across reruns.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine every time you click a button on a webpage, the entire page reloads from scratch. That is what Streamlit does — it reruns the whole Python script on every interaction. Session state is like a sticky note that survives those reloads, so you can remember things like the secret number, the score, or how many attempts the player has used.

- What change did you make that finally gave the game a stable secret number?
  The secret was already stored in `st.session_state` in the original code, so it was stable during a single game. The bug was that the New Game button used a hardcoded `random.randint(1, 100)` instead of `random.randint(low, high)`, which ignored the selected difficulty. Fixing that line made the secret respect the difficulty range and reset correctly on new games.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  I want to keep using placeholder-based rendering (`st.empty()`) whenever I need UI elements to reflect state that gets updated later in the script. This pattern of separating where something appears from when it gets its data is a useful technique beyond just Streamlit.

- What is one thing you would do differently next time you work with AI on a coding task?
  I would describe the bug more precisely upfront, including what I expected to happen and what actually happened. Several times Claude identified the right bug but I had to clarify details like "I don't want to move the position of the element." Being more specific earlier would have saved steps.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project showed me that AI-generated code can look completely correct on the surface but contain subtle logic bugs that only appear during actual use. I now treat AI-generated code as a starting draft that still needs careful human testing rather than a finished product.
