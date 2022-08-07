# import module
import streamlit as st
import pandas as pd
from datetime import date

# Read in data
predictions = pd.read_json(
    'https://github.com/nishalsach/lead_generation_app/blob/main/predicted_data_sample.json', 
    orient='records')

# Today's date
today = date.today()
# Get relative dates
two_weeks_ago = today - pd.Timedelta(days=14)
two_months_ago = today - pd.Timedelta(days=60)
six_months_ago = today - pd.Timedelta(days=180)
# Make dictionary of relative dates
date_dict = {
    'Last two weeks': two_weeks_ago,
    'Last two months': two_months_ago,
    'Last six months': six_months_ago
}

# Title
st.title("arXiv Lead Recommender")

# Time range buttons
time_range = st.radio(
    "Select time range for leads", 
    ("Last two weeks", "Last two months", "Last six months"))

# Start date
start_date = date_dict[time_range]

# Multiselect box for venues
 
# first argument takes the box title
# second argument takes the options to show
st.markdown("#### Select upto 3 news venues you would like to write for: ")
venues = st.multiselect(
    "",
    ['MIT Technology Review', 'Wired', 'VentureBeat'])


