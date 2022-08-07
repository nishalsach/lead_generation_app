# Library Imports
import streamlit as st
import pandas as pd
from datetime import date
import datetime
import article_card as ac

# Read in data
predictions = pd.read_json(
    'predicted_data_sample_latest.json', 
    orient='records')
# predictions = pd.read_csv(
#     'predicted_data_sample_latest.csv')

# Convert date
predictions['published'] = predictions['published'].apply(
    lambda x: datetime.datetime.fromtimestamp(int(x)/1000).date()
)

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
    'arxiv_all_categories', 'published', 'code_mentioned', 'readability',
    'title', 'summary', 'completion1', 'completion2', 'completion3', 
    'predicted_newsworthiness']

# Title
st.title("arXiv News Discovery Engine")
st.markdown("""---""")

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

# Run app
if start_date and venues_col_names:

    # Filter data
    predictions_filtered = predictions.loc[
        predictions['published'] >= start_date
    ][metadata_col_names + venues_col_names]

    # Scoring on relevance
    predictions_filtered['relevance_score'] = predictions_filtered[venues_col_names].mean(axis=1)

    # Overall scoring
    predictions_filtered['ranking_score'] = (predictions_filtered['relevance_score'] + predictions_filtered['predicted_newsworthiness']) / 2

    # Sort by overall score
    predictions_filtered = predictions_filtered.sort_values(by='ranking_score', ascending=False)
    
    # Reset index
    predictions_filtered = predictions_filtered.reset_index(drop=True)

    # Fill in article cards
    article_cards = []
    for i in range(len(predictions_filtered)):
        article = ac.articleCard()
        article.set_arxiv_id(predictions_filtered.loc[i, 'arxiv_id'])
        article.set_title(predictions_filtered.loc[i, 'title'])
        article.set_summary(predictions_filtered.loc[i, 'summary'])
        article.set_published(predictions_filtered.loc[i, 'published'])
        article.set_arxiv_url(predictions_filtered.loc[i, 'arxiv_url'])
        article.set_arxiv_primary_category(predictions_filtered.loc[i, 'arxiv_primary_category'])
        article.set_arxiv_all_categories(predictions_filtered.loc[i, 'arxiv_all_categories'])
        article.set_code_mentioned(predictions_filtered.loc[i, 'code_mentioned'])
        article.set_readability(predictions_filtered.loc[i, 'readability'])
        article.set_completion1(predictions_filtered.loc[i, 'completion1'])
        article.set_completion2(predictions_filtered.loc[i, 'completion2'])
        article.set_completion3(predictions_filtered.loc[i, 'completion3'])
        article.set_predicted_newsworthiness(predictions_filtered.loc[i, 'predicted_newsworthiness'])
        article_cards.append(article)
    

    # Display article cards
    for article in article_cards:

        article.show()


