"""Exercise 3 — improved version of the Questions page (pages/2_Questions.py).

UX improvements
- The expression is checked BEFORE saving: malformed input ("2 +", "1/0",
  "2^3") shows a clear error message instead of crashing the page or saving
  an unanswerable question with a NaN answer into the database.
- Live answer preview while composing the question.
- Success message after a question is created (the old page gave no feedback).
- Friendly tables with named columns and empty-state messages.

Code-quality improvements
- Helper functions (read_sheet / write_sheets / safe_evaluate) replace the
  copy-pasted pandas boilerplate; each has one job and a docstring.
- Constants for the database file and sheet names (no magic strings).
- Explicit error handling around EvaluateExpression.
- No leftover TODO comments, dead code, or redundant conditions.

The original page still works: both pages read and append to the same Excel
sheets with the same schema.
"""

import math

import pandas as pd
import streamlit as st

from library import EvaluateExpression

st.set_page_config(page_title="Improved Questions")

DB_FILE = "Mini Project 2 - Instructor Database.xlsx"
SHEET_USERS = "Users"
SHEET_QUESTIONS = "Questions"
SHEET_CHALLENGES = "Challenges"
SHEET_ASSOC = "Challenge-Users"


def read_sheet(sheet_name):
    """Read one worksheet of the database into a DataFrame."""
    return pd.read_excel(DB_FILE, sheet_name=sheet_name)


def write_sheets(named_frames):
    """Write every {sheet name: DataFrame} pair back into the database."""
    with pd.ExcelWriter(DB_FILE, mode="a", if_sheet_exists="replace") as writer:
        for sheet_name, frame in named_frames.items():
            frame.to_excel(writer, sheet_name=sheet_name, index=False)


def safe_evaluate(expression):
    """Evaluate a math expression without ever crashing the page.

    Returns (answer, error): on success error is None, on failure answer is
    None and error is a human-readable message.
    """
    if not expression.strip():
        return None, "The expression is empty."
    evaluator = EvaluateExpression(expression)
    if evaluator.expression == "":
        return None, "Invalid characters: only digits, + - * / ( ) . and spaces are allowed."

    # structural check: a valid infix expression has exactly one more operand
    # than operators, so inputs like "2 3" cannot silently evaluate to 3
    tokens = evaluator.insert_space().split()
    operands = [t for t in tokens if t not in "+-*/()"]
    operators = [t for t in tokens if t in "+-*/"]
    if len(operands) != len(operators) + 1:
        return None, "Incomplete expression: every operator needs a number on both sides."

    try:
        answer = evaluator.evaluate()
    except IndexError:
        return None, "Malformed expression: check that operators and brackets are complete."
    except ZeroDivisionError:
        return None, "Division by zero is undefined."
    except ValueError:
        return None, "Malformed number in the expression."
    if answer is None or not math.isfinite(answer):
        return None, "The result is too large to store as an answer."
    return answer, None


def create_question(expression, answer, selected_users, users):
    """Append the new question, its challenge, and one row per challenged user."""
    questions = read_sheet(SHEET_QUESTIONS)
    challenges = read_sheet(SHEET_CHALLENGES)
    assoc = read_sheet(SHEET_ASSOC)

    question_id = len(questions)
    challenge_id = len(challenges)
    questions.loc[question_id] = [question_id, expression, answer]
    challenges.loc[challenge_id] = [challenge_id, question_id]

    assoc_id = len(assoc)
    for username in selected_users:
        user_id = int(users.loc[users["username"] == username, "id"].iloc[0])
        assoc.loc[assoc_id] = [assoc_id, challenge_id, user_id]
        assoc_id += 1

    write_sheets({
        SHEET_QUESTIONS: questions,
        SHEET_CHALLENGES: challenges,
        SHEET_ASSOC: assoc,
    })


# --- page ---

st.header("Questions (Improved)")
st.caption(
    "Improved version of the Questions page for Exercise 3. "
    "The original page still works; both share the same database."
)

# reset the form BEFORE its widgets are created (Streamlit forbids writing a
# widget's state after it is instantiated in the same run)
if st.session_state.pop("clear_form", False):
    st.session_state["expr_input"] = ""
    st.session_state["user_select"] = []

# show feedback from the previous run, so the tables above stay fresh
if st.session_state.get("flash"):
    st.success(st.session_state.flash)
    st.session_state.flash = None

st.subheader("Questions List")
question_data = read_sheet(SHEET_QUESTIONS)
if question_data.empty:
    st.info("No questions yet. Create the first one below.")
else:
    # astype(str): the instructor database contains an Excel-coerced datetime
    # ("2-1" typed in Excel became 2025-02-01) — normalise so display never breaks
    st.dataframe(
        question_data.astype({"expression": str}).rename(
            columns={"id": "No.", "expression": "Question", "answer": "Answer"}
        ),
        hide_index=True,
    )

st.subheader("Create New Question")
expression = st.text_input(
    "Math expression:",
    key="expr_input",
    placeholder="e.g. (1 + 2) * 3",
    help="Allowed: digits, + - * / ( ) . and spaces",
)

answer, error = (None, None)
if expression:
    answer, error = safe_evaluate(expression)
    if error:
        st.error(error)
    else:
        st.success(f"Answer preview: {answer:g}")

users = read_sheet(SHEET_USERS)
selected_users = st.multiselect(
    "Send this challenge to:",
    users["username"],
    key="user_select",
    placeholder="Choose one or more users",
)

can_create = bool(expression) and error is None and len(selected_users) > 0
if not can_create:
    st.caption("Enter a valid expression and pick at least one user to enable the button.")

if st.button("Create Question", type="primary", disabled=not can_create):
    try:
        create_question(expression, answer, selected_users, users)
    except PermissionError:
        st.error(
            "Could not save: the Excel database is open in another program. "
            "Close it and try again."
        )
    else:
        st.session_state.flash = (
            f"Question '{expression}' created and sent to "
            f"{len(selected_users)} user(s): {', '.join(selected_users)}."
        )
        st.session_state.clear_form = True
        st.rerun()
