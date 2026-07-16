import streamlit as st
from library import EvaluateExpression
from expression_utils import safe_evaluate
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"

# Read user table
users = pd.read_excel(filename, sheet_name="Users")

# TODO: Task 1
# read the sheet with the name "Questions"
#
question_data = pd.read_excel(filename, sheet_name="Questions")

st.header("Questions List")
st.write(question_data)

st.header("Create New Question")
with st.form("new_question"):
    expression = st.text_input("Write a Math expression:")

    # TODO: Tasks 2 and 3
    # The EvaluateExpression object is created and its evaluate() method is
    # called inside safe_evaluate() (see expression_utils.py). The wrapper
    # adds edge-case handling so any input — "2 +", "1/0", "2^3", "2 3",
    # "-2+3" — shows a message or a correct answer instead of crashing.
    answer, error = safe_evaluate(expression)

    if expression and error:
        st.error(error)
    elif expression:
        st.write("Answer:", answer)

    selected_users = st.multiselect("Select Users to answer this challenge.", users["username"])
    submit = st.form_submit_button("Create Question")

if submit and error is None and selected_users:
    # TODO: Task 4
    # read Challenges and Challenge-Users tables
    # from the Excel file to update
    #
    challenge_data = pd.read_excel(filename, sheet_name="Challenges")
    assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")

    question_id = len(question_data)
    challenge_id = len(challenge_data)
    assoc_id = len(assoc_data)
    question_data.loc[question_id] = [question_id, expression, answer]
    challenge_data.loc[challenge_id] = [challenge_id, question_id]

    for user in selected_users:
        user_id = int(users.loc[users["username"] == user, "id"].iloc[0])
        assoc_data.loc[assoc_id] = [assoc_id, challenge_id, user_id]
        assoc_id += 1

    with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
        # TODO: Task 5
        # update the Excel file with the new data
        #
        question_data.to_excel(f, sheet_name="Questions", index=False)
        challenge_data.to_excel(f, sheet_name="Challenges", index=False)
        assoc_data.to_excel(f, sheet_name="Challenge-Users", index=False)

    st.rerun()
elif submit and expression and error is None and not selected_users:
    st.warning("Select at least one user to challenge.")
