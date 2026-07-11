import streamlit as st
from library import EvaluateExpression
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"

# Read user table
users = pd.read_excel(filename, sheet_name="Users")

# TODO: Task 1
# read the sheet with the name "Questions"
#
# question_data = None
### your code ###

st.header("Questions List")
st.write(question_data)

st.header("Create New Question")
with st.form("new_question"):
    expression = st.text_input("Write a Math expression:")
    expression

    # TODO: Task 2
    # create an object instance of EvaluateExpression class
    # pass on the math expression to the object
    #
    # evaluator = None
    ### your code ###

    # TODO: Task 3
    # call the evaluate() method of the EvaluateExpression object
    # and store it
    #
    # answer = None
    ### your code ###

    st.write("Answer:", answer)

    selected_users = st.multiselect("Select Users to answer this challenge.", users["username"])
    submit = st.form_submit_button("Create Question")

if submit and expression and expression != "" and selected_users != []:
    # TODO: Task 4
    # read Challenges and Challenge-Users tables 
    # from the Excel file to update
    #
    # read the Challenges worksheet into challenge_data variable
    # challenge_data = None
    ### your code ###

    #
    # read the Challenge-Users worksheet into assoc_data variable
    # assoc_data = None
    ### your code ###

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
        pass
        # TODO: Task 5
        # update the Excel file with the new data
        #
        # update the Questions worksheet
        # question_data.to_excel(...)
        ### your code ###

        #
        # update the Challenges worksheet
        # challenge_data.to_excel(...)
        ### your code ###
        #
        # update the Challenge-Users worksheet
        # assoc_data.to_excel(...)
        ### your code ###

    # st.cache_data.clear()
    st.rerun()

            


