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
title_container = st.container()
with title_container:
    st.title("arXiv News Discovery Engine")
    st.markdown("""---""")

# Using "with" notation
with st.sidebar:
    st.header("Date and Venue Filters")
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

    # Fill in article cards
    article_cards = []
    for i in range(len(predictions)):
        article = ac.articleCard()
        article.set_arxiv_id(predictions.loc[i, 'arxiv_id'])
        article.set_title(predictions.loc[i, 'title'])
        article.set_summary(predictions.loc[i, 'summary'])
        article.set_published(predictions.loc[i, 'published'])
        article.set_arxiv_url(predictions.loc[i, 'arxiv_url'])
        article.set_arxiv_primary_category(predictions.loc[i, 'arxiv_primary_category'])
        article.set_arxiv_all_categories(predictions.loc[i, 'arxiv_all_categories'])
        article.set_code_mentioned(predictions.loc[i, 'code_mentioned'])
        article.set_readability(predictions.loc[i, 'readability'])
        article.set_completion1(predictions.loc[i, 'completion1'])
        article.set_completion2(predictions.loc[i, 'completion2'])
        article.set_completion3(predictions.loc[i, 'completion3'])
        article.set_predicted_newsworthiness(predictions.loc[i, 'predicted_newsworthiness'])
        article_cards.append(article)
    
    # Make a container for the articles
    articles_container = st.container()
    with articles_container:
        # Display article cards
        for article in article_cards:
            article.show()
    
    # Scroll up
    st.markdown("[Go back to the top.](#arxiv-news-discovery-engine)")

