# import module
import streamlit as st
import pandas as pd
from datetime import date

# Read in data
predictions = pd.read_json(
    'predicted_data_sample_latest.json', 
    orient='records')

# Set some variables
venues_col_names = []
start_date = None

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

# List of metadata columns
metadata_col_names = [
    'arxiv_id', 'arxiv_url', 'arxiv_primary_category', 
    'arxiv_all_categories', 'published', 'code_mentioned', 'readability'
    'title', 'summary', 'completion1', 'completion2', 'completion3', 
    'predicted_newsworthiness']

# Title
st.title("arXiv Lead Recommender")



# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    time_range = st.radio(
        "Select time range for leads:", 
    ("Last two weeks", "Last two months", "Last six months"))
    venues = st.multiselect(
    "Select upto 3 news venues you would like to write for: ",
    ['MIT Technology Review', 'Wired', 'VentureBeat'])

# Start date and venue col names
start_date = date_dict[time_range]
venues_col_names = [source_dict[venue] for venue in venues]

# Filter on date and venues
if start_date and venues_col_names:
    predictions = predictions.loc[
        predictions['published'] >= start_date
    ][metadata_col_names + venues_col_names]
    # Scoring on relevance
    predictions['relevance_score'] = predictions[venues_col_names].mean(axis=1)
    # Overall scoring
    predictions['ranking_score'] = (predictions['relevance_score'] + predictions['predicted_newsworthiness']) / 2
    # Sort by overall score
    predictions = predictions.sort_values(by='ranking_score', ascending=False)
    # Reset index
    predictions = predictions.reset_index(drop=True)
    # Display in streamlit
    st.write(predictions)


