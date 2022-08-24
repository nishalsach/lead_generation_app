# Library Imports
import streamlit as st
import pandas as pd
import datetime
import article_card_similarity as ac

# Read in and cache this dataframe
@st.cache
def get_data():
    return pd.read_json(
        '220101_onwards_all_predictions_sample_300.json', 
        orient='records').sample(150).reset_index(drop=True)
predictions = get_data()

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
    'Ars Technica': 'ars_technica',
    'Futurism': 'futurism',
    'MIT Technology Review': 'technologyreview',
    'New Scientist': 'newscientist',
    'New York Times': 'nytimes',
    'Popular Science': 'popsci', 
    'Popular Mechanics' : 'popularmechanics',
    'Quartz': 'quartz',
    'Salon': 'salon',
    'ScienMag': 'scienmag',
    'Scientific American': 'scientificamerican',
    'StatNews': 'statnews',
    'TechCrunch': 'techcrunch',
    'The Conversation': 'theconversation',
    'VentureBeat': 'venturebeat',
    'Vice News': 'vice',
    'Vox': 'vox',
    'Washington Post': 'washingtonpost',
    'Wired': 'wired',
    
}

# List of metadata columns
metadata_col_names = [
    'arxiv_id', 
    'arxiv_url', 
    'arxiv_primary_category', 
    'published', 
    'published_hr', 
    'arxiv_primary_category_hr',
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

    # Instructions for users
    st.header("Instructions")
    st.write("You can interact with the controls below to refine the recommendations of the tool.")
    
    # Date filter
    st.header("Filter on Date of Publication")
    time_range = st.selectbox(
        label = "Pubiication date for arXiv articles:",
        options = ("None", "Last two weeks", "Last two months", "Last six months"))

    # Outlet filter
    st.header("Select News Outlets")
    venues = st.multiselect(
        label = "Select upto 3 news outlets you are interested in writing for.",
        options = [
            'Ars Technica',
            'Futurism',
            'MIT Technology Review',
            'New Scientist',
            'New York Times',
            'Popular Science',
            'Popular Mechanics',
            'Quartz',
            'Salon',
            'ScienMag',
            'Scientific American',
            'StatNews',
            'TechCrunch',
            'The Conversation',
            'VentureBeat',
            'Vice News',
            'Vox',
            'Washington Post',
            'Wired'
            ], 
        help = 'Items will be ranked on their relevance to the selected outlets. If no outlets are selected, items will be ranked by newsworthiness scores instead.', 
        default=None)
    
    # Newsworthiness filter
    st.header("Filter on Newsworthiness")
    min_newsworthiness = st.slider(
        "Show articles with a newsworthiness score above:",
        min_value=0, 
        max_value=95,
        value=50, 
        step=5
    )
    # # delete this with updates on data
    # min_newsworthiness = min_newsworthiness/100
    # Scroll up
    st.markdown("[Scroll results back to the top.](#arxiv-news-discovery-engine)")


# Conditions to display dummy item
if time_range=="None":
    st.write("Instructions/Dummy Item go here")

# Full item display
if time_range!="None":

    # Put in a start date
    start_date = date_dict[time_range]
    # Filter by date
    predictions_filtered = predictions.loc[
        predictions['published'] >= start_date
    ].copy()

    # Filter by newsworthiness
    predictions_filtered = predictions_filtered.loc[
        predictions_filtered['predicted_newsworthiness'] >= min_newsworthiness
    ]
    # Reset index
    predictions_filtered.reset_index(drop=True, inplace=True)

    # Check for venues:
    if venues:

        # Put in the venues
        venues_col_names = [source_dict[venue] for venue in venues]
        # Filter by venues
        predictions_filtered = predictions_filtered[
            metadata_col_names + venues_col_names]

        # Scoring on relevance
        predictions_filtered['outlet_relevance'] = predictions_filtered[venues_col_names].mean(axis=1)
        # Sort by overall score
        predictions_filtered = predictions_filtered.sort_values(by='outlet_relevance', ascending=False)
        # Reset index
        predictions_filtered = predictions_filtered.reset_index(drop=True)

    # Otherwise just sort by newsworthiness and show
    else:

        predictions_filtered.sort_values(by='predicted_newsworthiness', ascending=False, inplace=True)
        predictions_filtered = predictions_filtered.reset_index(drop=True)

    # Fill in article cards
    article_cards = []

    for i in range(len(predictions_filtered)):
        article = ac.articleCard()
        # Metadata
        article.set_arxiv_id(predictions_filtered.loc[i, 'arxiv_id'])
        article.set_title(predictions_filtered.loc[i, 'title'])
        article.set_summary(predictions_filtered.loc[i, 'summary'])
        article.set_published(predictions_filtered.loc[i, 'published'])
        article.set_published_hr(predictions_filtered.loc[i, 'published_hr'])
        article.set_arxiv_url(predictions_filtered.loc[i, 'arxiv_url'])
        article.set_arxiv_primary_category(predictions_filtered.loc[i, 'arxiv_primary_category'])
        article.set_arxiv_primary_category_hr(predictions_filtered.loc[i, 'arxiv_primary_category_hr'])

        # Angles
        article.set_completion1(predictions_filtered.loc[i, 'completion1'])
        article.set_completion2(predictions_filtered.loc[i, 'completion2'])
        article.set_completion3(predictions_filtered.loc[i, 'completion3'])

        # Metrics
        article.set_predicted_newsworthiness(predictions_filtered.loc[i, 'predicted_newsworthiness'])
        article.set_outlet_relevance(predictions_filtered.loc[i, 'outlet_relevance'])
        article_cards.append(article)

    # Display articles
    for article in article_cards:
        article.show()

        


