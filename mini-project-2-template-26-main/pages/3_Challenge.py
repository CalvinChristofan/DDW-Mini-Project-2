import streamlit as st
import time
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"

users = pd.read_excel(filename, sheet_name='Users')
challenges = pd.read_excel(filename, sheet_name="Challenges")
questions = pd.read_excel(filename, sheet_name="Questions")
assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")

if 'elapsed_time' not in st.session_state or 'answer_correctness' not in st.session_state:
    st.session_state["elapsed_time"] = None
    st.session_state["answer_correctness"] = None

current_user = st.selectbox("Select a User:", users["username"])
current_user_id = int(users.loc[users["username"] == current_user,"id"].iloc[0])
challenges_id_list = assoc_data.loc[assoc_data["user_id"] == current_user_id,"challenge_id"]
challenges_id_list = [int(id) for id in challenges_id_list ]
question = None
user_answer = None


def start_timer():
    st.session_state["start_time"] = time.time()

def end_timer():
    st.session_state["end_time"] = time.time()

def clear_answer():
    st.session_state.user_answer = None
    

with st.form("take_challenge"):
    challenge_no = st.selectbox("Select a Challenge:", [c_id + 1 for c_id in challenges_id_list])
    submit = st.form_submit_button("Take Challenge", on_click=start_timer)

if submit and current_user is not None and challenge_no is not None:
    challenge_id = challenge_no - 1
    question_id = int(challenges.loc[challenges["id"] == challenge_id, "question_id"].iloc[0])
    question = questions.loc[questions["id"] == question_id, "expression"].iloc[0]
    st.session_state["correct_answer"] = questions.loc[questions["id"] == question_id, "answer"].iloc[0]

st.write("Question: ", question)

with st.form("answer"):
    user_answer = st.number_input("Answer: ", value=None, key="user_answer")
    submit_answer = st.form_submit_button("Submit", on_click=end_timer)
    clear_answer = st.form_submit_button("Clear", on_click=clear_answer)


if submit_answer:
    challenge_id = challenge_no - 1
    if user_answer == st.session_state.correct_answer:
        end_time = st.session_state["end_time"]
        start_time = st.session_state["start_time"]
        elapsed_time = int(end_time - start_time)
        timerecord = pd.read_excel(filename, sheet_name="Timerecord")
        timerecord_id = len(timerecord)
        timerecord.loc[timerecord_id] = [timerecord_id, challenge_id, current_user_id, elapsed_time]
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
            timerecord.to_excel(f, sheet_name="Timerecord", index=False)
        user_answer = None
        st.session_state["answer_correctness"] = True
        st.session_state["correct_answer"] = None
        st.session_state["elapsed_time"] = elapsed_time
    else:
        st.session_state["answer_correctness"] = False
    # st.cache_data.clear()
    st.rerun()

if st.session_state.answer_correctness == False:
    st.text("You entered a wrong answer.")
    st.session_state["elapsed_time"] = None
    st.session_state["answer_correctness"] = None
elif st.session_state.answer_correctness: 
    elapsed_time = st.session_state["elapsed_time"]
    st.text(f"You answered correctly within: {elapsed_time} seconds.")
    st.session_state["elapsed_time"] = None
    st.session_state["answer_correctness"] = None
else:
    st.text("You have not entered any answer.")    
    




        
        


