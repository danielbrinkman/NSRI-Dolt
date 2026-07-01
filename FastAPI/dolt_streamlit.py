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
        test = {
            'username' : st.session_state.auth['username'],
            'password' : st.session_state.auth['password'],
            'action' : 'auth',
        }
        resp = requests.post("http://127.0.0.1:8000/query/", json=test)
        if (resp.status_code==200) & (json.loads(resp.text)['authentication']):
            st.session_state.failed=False
            st.rerun()
        else:
            st.session_state.failed=True
            st.rerun()
    if failed:
        st.caption(":red[Failed to authenticate. Try again.]")

def load_page():
    st.title("Welcome to the Dolt EDB")
    # st.text(f"Authenticated! Your username is {st.session_state.auth['username']} and your password is {st.session_state.auth['password']}")
    if st.button("Get User Table"):
        query_table()

def query_table():
    content = {
        'username' : st.session_state.auth['username'],
        'password' : st.session_state.auth['password'],
        'action' : 'query',
        'query' : 'SELECT * FROM users',
    }
    resp = requests.post("http://127.0.0.1:8000/query/", json=content)
    if (resp.status_code==200) & (json.loads(resp.text)['authentication']):
        table = pd.read_json(json.loads(resp.text)['value'])
        return st.table(table)
    else:
        return st.caption(":red[Query failed.]")

if "auth" not in st.session_state:
    st.session_state.first_pass = True
    credentials()
else:
    if (st.session_state.first_pass) & (st.session_state.failed==False):
        st.session_state.first_pass = False
        st.toast("✅ User credentials confirmed.")
        load_page()
    elif (st.session_state.failed==False):
        load_page()
    else:
        credentials(failed=True)