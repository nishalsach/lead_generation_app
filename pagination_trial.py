import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = 1


st.title("Test")

if st.session_state.page == 1:
    st.write("Page 1")
elif st.session_state.page == 2:
    st.write("Page 2")
else:
    st.write("No page")

if st.button("Next"):
    st.session_state.page = 2

if st.button("Previous"):
    st.session_state.page = 1