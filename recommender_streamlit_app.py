# import module
import streamlit as st
import pandas as pd
from datetime import date

# Read in data
predictions = pd.read_json(
    'predicted_data_sample.json', 
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

# Dictionary of source-column names
source_dict = {
    'MIT Technology Review': 'technologyreview',
    'Wired': 'wired',
    'VentureBeat': 'venturebeat',
}

# Title
st.title("arXiv Lead Recommender")

# Time range buttons
# st.markdown("#### Select time range for leads: ")
time_range = st.radio(
    "Select time range for leads:", 
    ("Last two weeks", "Last two months", "Last six months"))

# Start date
start_date = date_dict[time_range]

# Multiselect box for venues
 
# first argument takes the box title
# second argument takes the options to show
# st.markdown("#### Select upto 3 news venues you would like to write for: ")
venues = st.multiselect(
    "Select upto 3 news venues you would like to write for: ",
    ['MIT Technology Review', 'Wired', 'VentureBeat'])
venues_col_names = [source_dict[venue] for venue in venues]

# 

