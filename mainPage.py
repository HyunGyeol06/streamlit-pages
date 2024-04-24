import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write(st.secrets["wtf"])

st.sidebar.success("Select a page above.")