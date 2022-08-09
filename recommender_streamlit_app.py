# Library Imports
import streamlit as st
import pandas as pd
import datetime
import article_card as ac

# Read in data
predictions = pd.read_json(
    'predicted_data_fake_news_angles_all_nw.json', 
    orient='records')

# # Convert date
# predictions['published'] = predictions['published'].apply(
#     lambda x: datetime.datetime.fromtimestamp(int(x)/1000).date()
# )

# Set some variables
venues_col_names = []
start_date = None

# Today's date
now = datetime.datetime.now().replace(microsecond=0)
# Get relative dates
two_weeks_ago = int(datetime.datetime.timestamp(now - pd.Timedelta(days=14))*1000)
two_months_ago = int(datetime.datetime.timestamp(now - pd.Timedelta(days=60))*1000)
six_months_ago = int(datetime.datetime.timestamp(now - pd.Timedelta(days=180))*1000)

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
    'New Scientist': 'newsscientist',
    'The Conversation': 'theconversation',
}

# List of metadata columns
metadata_col_names = [
    'arxiv_id', 
    'arxiv_url', 
    'arxiv_primary_category', 
    'arxiv_all_categories', 
    'published', 
    'code_mentioned', 
    'readability',
    'title', 
    'summary', 
    'completion1', 
    'completion2', 
    'completion3', 
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
        ['MIT Technology Review', 'New Scientist', 'The Conversation', 'VentureBeat', 'Wired', ])

# Check and run app
if time_range:
    # Put in a start date
    start_date = date_dict[time_range]
    # Filter by date
    predictions_result = predictions.loc[
        predictions['published'] >= start_date
    ].copy()
    # Reset index
    predictions_result.reset_index(drop=True, inplace=True)
    # Check for venues:
    if venues:
        # Put in the venues
        venues_col_names = [source_dict[venue] for venue in venues]
        # Filter by venues
        predictions_result = predictions_result[
            metadata_col_names + venues_col_names]

        # Scoring on relevance
        predictions_result['relevance_score'] = predictions_result[venues_col_names].mean(axis=1)
        # Overall scoring
        predictions_result['ranking_score'] = (predictions_result['relevance_score'] + predictions_result['predicted_newsworthiness']) / 2
        # Sort by overall score
        predictions_result = predictions_result.sort_values(by='ranking_score', ascending=False)
        # Reset index
        predictions_result = predictions_result.reset_index(drop=True)
    
    # Otherwise just sort by newsworthiness and show
    else:
        predictions_result = predictions_result.sort_values(by='predicted_newsworthiness', ascending=False)
        predictions_result = predictions_result.reset_index(drop=True)

    # Fill in article cards
    article_cards = []
    for i in range(len(predictions_result)):
        article = ac.articleCard()
        article.set_arxiv_id(predictions_result.loc[i, 'arxiv_id'])
        article.set_title(predictions_result.loc[i, 'title'])
        article.set_summary(predictions_result.loc[i, 'summary'])
        article.set_published(predictions_result.loc[i, 'published'])
        article.set_published_hr(predictions_result.loc[i, 'published_hr'])
        article.set_arxiv_url(predictions_result.loc[i, 'arxiv_url'])
        article.set_arxiv_primary_category(predictions_result.loc[i, 'arxiv_primary_category'])
        article.set_arxiv_primary_category_hr(predictions_result.loc[i, 'arxiv_primary_category_hr'])
        # article.set_arxiv_all_categories(predictions.loc[i, 'arxiv_all_categories'])
        # article.set_code_mentioned(predictions.loc[i, 'code_mentioned'])
        # article.set_readability(predictions.loc[i, 'readability'])
        article.set_completion1(predictions_result.loc[i, 'completion1'])
        article.set_completion2(predictions_result.loc[i, 'completion2'])
        article.set_completion3(predictions_result.loc[i, 'completion3'])
        article.set_predicted_newsworthiness(predictions_result.loc[i, 'predicted_newsworthiness'])
        article_cards.append(article)
    
    # Make a container for the articles
    articles_container = st.container()
    with articles_container:
        # Display article cards
        for article in article_cards:
            article.show()
    
    # Scroll up
    st.markdown("[Go back to the top.](#arxiv-news-discovery-engine)")

