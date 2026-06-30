import streamlit as st
import sqlalchemy
import pandas as pd
import json
import requests

engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:secret2@0.0.0.0:3307/edb")

@st.dialog("Provide your credentials")
def credentials(failed=False):
    username = st.text_input("Username...")
    password = st.text_input("Password...", type="password")
    if st.button("Submit"):
        st.session_state.auth = {"username": username, "password": password}
        st.rerun()    
    if failed:
        st.caption(":red[Failed to authenticate. Try again.]")

if "auth" not in st.session_state:
    credentials()
else:
    test = {
        'username' : st.session_state.auth['username'],
        'password' : st.session_state.auth['password'],
        'action' : 'auth',
    }

    resp = requests.post("http://127.0.0.1:8000/query/", json=test)
    if resp.status_code==200:
        if json.loads(resp.text)['authentication']:
            f"Authenticated! Your username is {st.session_state.auth['username']} and your password is {st.session_state.auth['password']}"
        else:
            credentials(failed=True)