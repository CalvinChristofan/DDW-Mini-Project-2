import streamlit as st
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"

users = pd.read_excel(filename, sheet_name='Users')
challenges = pd.read_excel(filename, sheet_name="Challenges")
questions = pd.read_excel(filename, sheet_name="Questions")
assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")
timerecords = pd.read_excel(filename, sheet_name="Timerecord")

df_challenge = challenges.merge(questions, left_on="question_id", right_on="id")
df_challenge_time = df_challenge.merge(timerecords, left_on="id_x", right_on="challenge_id")

df_challenge_time = df_challenge_time.drop(columns=['id_x', 'id_y', 'id'])

df_challenge_users_names = df_challenge_time.merge(users, left_on="user_id", right_on="id")

df_challenge_users_names = df_challenge_users_names.drop(columns=['user_id', 'id'])

df_challenge_users_names = df_challenge_users_names[['challenge_id', 'expression', 'answer', 'name', 'elapsed_time']]

df_sorted = df_challenge_users_names.sort_values(by=['challenge_id', 'elapsed_time']).rename(columns={"challenge_id": "Challenge No.",
                                                                                                      "expression": "Question",
                                                                                                      "answer": "Correct Answer",
                                                                                                      "name": "Name",
                                                                                                      "elapsed_time": "Elapsed Time (s)"}
)

for challenge in df_sorted['Challenge No.'].unique():
    st.header(f"Challenge No: {challenge + 1:.0f}")
    records = df_sorted[df_sorted["Challenge No."] == challenge]
    st.write(f"Question: {records['Question'].iloc[0]:s}")
    st.write(f"Answer: {records['Correct Answer'].iloc[0]:.2f}")
    st.write("Top Three Users:")
    st.write(records.nsmallest(n=3, columns=['Elapsed Time (s)'], keep='all').drop(columns=['Challenge No.', 'Question', 'Correct Answer']))



