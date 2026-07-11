import streamlit as st
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")
users

with st.form("new_user", clear_on_submit=True):
    new_username = st.text_input("New Username:")
    new_name = st.text_input("Full Name:")

    submit = st.form_submit_button("Update User Table")

if submit:
    if new_username and new_name:
        users.loc[len(users)] = [len(users), new_username, new_name]
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
            users.to_excel(f, sheet_name="Users", index=False)
        # st.cache_data.clear()
        st.rerun()


