# import module
import streamlit as st
 
# Title
st.title("arXiv Lead Recommender")

# multi select box for venues
 
# first argument takes the box title
# second argument takes the options to show
st.markdown("### Select upto 3 news venues you would like to write for: ")
venues = st.multiselect(
    "",
    ['MIT Technology Review', 'Wired', 'VentureBeat'])


