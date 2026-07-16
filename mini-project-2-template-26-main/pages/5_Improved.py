"""Exercise 3: improved version of the Questions page (2_Questions.py).
UX: live answer preview, clear error messages, metrics, search, history.
Code quality: shared validation module, helpers, constants, error handling."""

import pandas as pd
import streamlit as st

from expression_utils import safe_evaluate

st.set_page_config(page_title="Improved Questions")

# code quality: constants defined once instead of retyping strings everywhere
DB_FILE = "Mini Project 2 - Instructor Database.xlsx"
SHEET_USERS = "Users"
SHEET_QUESTIONS = "Questions"
SHEET_CHALLENGES = "Challenges"
SHEET_ASSOC = "Challenge-Users"


# code quality: one helper replaces the pd.read_excel boilerplate on every page (DRY)
def read_sheet(sheet_name):
    return pd.read_excel(DB_FILE, sheet_name=sheet_name)


# code quality: one writer for any number of sheets
def write_sheets(named_frames):
    with pd.ExcelWriter(DB_FILE, mode="a", if_sheet_exists="replace") as writer:
        for sheet_name, frame in named_frames.items():
            frame.to_excel(writer, sheet_name=sheet_name, index=False)


# code quality: the whole save is one single-purpose function, not inline page code
def create_question(expression, answer, selected_users, users):
    questions = read_sheet(SHEET_QUESTIONS)
    challenges = read_sheet(SHEET_CHALLENGES)
    assoc = read_sheet(SHEET_ASSOC)

    # new ids continue from the current row count
    question_id = len(questions)
    challenge_id = len(challenges)
    questions.loc[question_id] = [question_id, expression, answer]
    challenges.loc[challenge_id] = [challenge_id, question_id]

    # one Challenge-Users row per selected user
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


st.header("Questions (Improved)")
st.caption(
    "Improved version of the Questions page for Exercise 3. "
    "The original page still works; both share the same database."
)

# reset the form before its widgets are created (Streamlit forbids it afterwards)
if st.session_state.pop("clear_form", False):
    st.session_state["expr_input"] = ""
    st.session_state["user_select"] = []

# show the success message saved by the previous run
if st.session_state.get("flash"):
    st.success(st.session_state.flash)
    st.session_state.flash = None

# read all four tables once
users = read_sheet(SHEET_USERS)
question_data = read_sheet(SHEET_QUESTIONS)
challenge_data = read_sheet(SHEET_CHALLENGES)
assoc_data = read_sheet(SHEET_ASSOC)

# dashboard metrics
m_questions, m_challenges, m_players = st.columns(3)
m_questions.metric("Questions", len(question_data))
m_challenges.metric("Challenges sent", len(challenge_data))
m_players.metric("Players", len(users))

# questions table with a search filter and friendly column names
st.subheader("Questions List")
if question_data.empty:
    st.info("No questions yet. Create the first one below.")
else:
    display = question_data.astype({"expression": str})  # guards against Excel-coerced cells
    search = st.text_input("Search questions:", placeholder="type to filter, e.g. 3 +")
    if search:
        display = display[display["expression"].str.contains(search, case=False, regex=False)]
    if display.empty:
        st.info("No questions match your search.")
    else:
        st.dataframe(
            display.rename(columns={"id": "No.", "expression": "Question", "answer": "Answer"}),
            hide_index=True,
        )

# challenge history: which users received each challenge
with st.expander("Challenge history — who received which question"):
    if assoc_data.empty:
        st.info("No challenges sent yet.")
    else:
        # lookup tables: user id -> username, challenge id -> question id -> text
        names = users.set_index("id")["username"].astype(str)
        question_of = challenge_data.set_index("id")["question_id"]
        text_of = question_data.set_index("id")["expression"].astype(str)

        history = (
            assoc_data.groupby("challenge_id")["user_id"]
            .apply(lambda ids: ", ".join(names.reindex(ids).fillna("(deleted user)")))
            .reset_index(name="Sent to")
        )
        history["Question"] = history["challenge_id"].map(question_of).map(text_of)
        history["challenge_id"] += 1  # match the numbering on the Challenge page
        history = history.rename(columns={"challenge_id": "Challenge No."})
        st.dataframe(history[["Challenge No.", "Question", "Sent to"]], hide_index=True)

# create-question form with a live answer preview
st.subheader("Create New Question")
expression = st.text_input(
    "Math expression:",
    key="expr_input",
    placeholder="e.g. (1 + 2) * 3",
    help="Allowed: digits, + - * / ( ) . and spaces. Negative numbers are supported.",
)

# code quality: validation lives once in expression_utils.py, shared with 2_Questions.py
answer, error = (None, None)
if expression:
    answer, error = safe_evaluate(expression)
    if error:
        st.error(error)
    else:
        st.success(f"Answer preview: {answer:g}")
        if expression.strip() in set(question_data["expression"].astype(str).str.strip()):
            st.info("An identical question already exists. Creating it again will duplicate it.")

selected_users = st.multiselect(
    "Send this challenge to:",
    users["username"],
    key="user_select",
    placeholder="Choose one or more users",
)

# the button unlocks only when the input is valid, so bad data can never be saved
can_create = bool(expression) and error is None and len(selected_users) > 0
if not can_create:
    st.caption("Enter a valid expression and pick at least one user to enable the button.")

if st.button("Create Question", type="primary", disabled=not can_create):
    # code quality: even a locked Excel file shows a message instead of a crash
    try:
        create_question(expression, answer, selected_users, users)
    except PermissionError:
        st.error("Could not save: the Excel database is open in another program. Close it and try again.")
    else:
        st.session_state.flash = (
            f"Question '{expression}' created and sent to "
            f"{len(selected_users)} user(s): {', '.join(selected_users)}."
        )
        st.session_state.clear_form = True
        st.rerun()
