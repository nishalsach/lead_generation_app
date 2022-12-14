# Library Imports
import streamlit as st
import pandas as pd
import datetime
import article_card_similarity as acs
import article_card_newsworthiness as acn
import math
from sklearn.preprocessing import MinMaxScaler
from PIL import Image

def next_page():
    st.session_state.page += 1
def prev_page():
    st.session_state.page -= 1

# Read in and cache this dataframe
# @st.cache
def get_data():
    return pd.read_json(
        '220101_onwards_arxiv_predictions_display.json',
        # '220101_onwards_arxiv_predictions_display_10_latest.json',
        # '220101_onwards_all_predictions_sample_300.json', 
        orient='records').reset_index(drop=True)
predictions = get_data()

# Read in and cache an image
# @st.cache
def get_dummy_image():
    return Image.open('dummy_image.png')

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
    'Ars Technica': 'arstechnica',
    'Futurism': 'futurism',
    'MIT Technology Review': 'technologyreview',
    'New Scientist': 'newscientist',
    'New York Times': 'nytimes',
    'Popular Science': 'popsci', 
    'Popular Mechanics' : 'popularmechanics',
    'Quartz': 'quartz',
    'Salon': 'salon',
    # 'ScienMag': 'scienmag',
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

# Pagination var
page_size = 20

# Title
title_container = st.container()
with title_container:
    # title_col1, title_col2, title_col3 = st.columns([1, 10, 1])
    st.markdown(
        "<h1 style='text-align:center'> arXiv News Discovery Engine </h2>", unsafe_allow_html=True)
    st.markdown("""---""")

# Making the sidebar
with st.sidebar:

    # Instructions for users
    st.header("Instructions")
    st.write("You can interact with the controls below to refine the recommendations of the tool.")
    
    # Date filter
    st.header("Filter on Date of Publication")
    time_range = st.selectbox(
        label = "Pubiication date for arXiv articles:",
        options = ("None", "Last two weeks", "Last two months", "Last six months"))

    # Newsworthiness filter
    st.header("Filter on Newsworthiness")
    min_newsworthiness = st.slider(
        "Show articles with a newsworthiness score above:",
        # Slider arguments for the 100 case
        # min_value=0, 
        max_value=95,
        value=50, 
        step=5

        # Slider arguments for the 10 case
        # min_value=0.0, 
        # max_value=9.5,
        # value=5.0, 
        # step=0.5

    )

    # Outlet filter
    st.header("Select News Outlets")
    venues = st.multiselect(
        label = "Select one or more news outlets that you are interested in writing for.",
        options = list(source_dict.keys()), 
        help = 'Items will be ranked on their relevance to the selected outlets. If no outlets are selected, items will be ranked by newsworthiness scores instead.', 
        default=None)
    
    
    # # Scroll up
    # st.markdown("[Scroll results back to the top.](#arxiv-news-discovery-engine)")

# Change session state variables and update page
if "time_range" not in st.session_state:
    st.session_state.time_range = time_range
elif st.session_state.time_range != time_range:
    st.session_state.time_range = time_range
    st.session_state.page = 0
if "venues" not in st.session_state:
    st.session_state.venues = venues
elif st.session_state.venues != venues:
    st.session_state.venues = venues
    st.session_state.page = 0
if "min_newsworthiness" not in st.session_state:
    st.session_state.min_newsworthiness = min_newsworthiness
elif st.session_state.min_newsworthiness != min_newsworthiness:
    st.session_state.min_newsworthiness = min_newsworthiness
    st.session_state.page = 0


# Conditions to display dummy item
if time_range=="None":
    
    # st.write(predictions.loc[0, 'published_hr'])

    st.markdown(
        "Welcome to the arXiv news discovery engine! This tool is designed to help you uncover the most newsworthy articles from the thousands that are published in the [arXiv preprint repository](https://arxiv.org). It specifically recommends articles from the field of Computer Science, as well as its intersections with other fields of impact.  \n\n  You can use the sidebar to  filter the arXiv articles by their **date of publication**. By default, the results you see are ranked by their **newsworthiness scores** that we calculated using an AI model. This score is calculated out of a hundred, and its design has been informed by the opinions and ideas of other journalists like you. The sidebar also lets you use the newsworthiness score to filter out articles. **The newsworthiness typically goes as high as an 80 or 90.** \n\n  Next, you can optionally select specific news outlets you are interested in pitching stories to. Our tool will then calculate an **outlet similarity score** for each arXiv article, based on its similarity to the past news coverage from your selected outlet(s). It will also rank articles on the basis of higher similarity scores. **The similarity scores typically go as high as a 40 or 50.** We recommend that these scores should be considered relative each other, instead of being compared to the newsworthiness.  \n\n  Along with its recommendations, the tool also provides a list of **news angles** that could be used to frame potential stories about the individual articles. These news angles were generated using [OpenAI's GPT-3](https://openai.com/api/) model. \n\n "
        )

    st.markdown("### Example of a recommended article")
    # Call the image
    st.image(
        get_dummy_image(), 
        caption='Click the top-right corner to expand the image.'
    )

    # (https://arxiv.org/list/cs/new)

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
        # # Scale to 0-100
        # scaler = MinMaxScaler()
        # predictions_filtered['outlet_relevance'] = scaler.fit_transform(
        #     predictions_filtered[['predictions_filtered']])
        # Sort by overall score
        predictions_filtered = predictions_filtered.sort_values(by='outlet_relevance', ascending=False)
        # Reset index
        predictions_filtered = predictions_filtered.reset_index(drop=True)

    # Otherwise just sort by newsworthiness and show
    else:

        predictions_filtered.sort_values(by='predicted_newsworthiness', ascending=False, inplace=True)
        predictions_filtered = predictions_filtered.reset_index(drop=True)
    
    # Pagination config
    if "page" not in st.session_state:
        st.session_state.page = 0
    
    # Print results only if there are results
    if predictions_filtered.shape[0] > 0:

        # Calculate max pages for this set of results
        max_pages = math.ceil(predictions_filtered.shape[0]/page_size)
        
        # Setup the top pagination
        pages_container = st.container()
        with pages_container:
            # Make columns for the pagination buttons - do I want to re-align this???
            _, col1, col2, col3, _ = st.columns([0.1, 0.13, 0.2, 0.1, 0.1])
            # Next page button if there's pages left
            if st.session_state.page+1 < max_pages:
                col3.button(">", on_click=next_page, key='next_top')
            # Emppty space if there's no next pages left
            else:
                col3.write("")  # this makes the empty column show up on mobile

            # Previous page button if there's pages left
            if st.session_state.page > 0:
                col1.button("<", on_click=prev_page, key='prev_top')
            # Emppty space if there's no previous pages left
            else:
                col1.write("")  # this makes the empty column show up on mobile
            # Current page number
            col2.write(f"Page {1+st.session_state.page} of {max_pages}")
            
        # Get a start index of dataframe for the current page
        start = page_size * st.session_state.page
        # Get an end index of dataframe for the current page
        if st.session_state.page == max_pages-1:
            end = predictions_filtered.shape[0]
        else:
            end = start + page_size

        # Change ordering of what metric's on top based on if venues are selected
        if venues:
            for i in range(start, end):
                article = acs.articleCardSimilarity()

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
                article.show()

        else: 
            for i in range(start, end):

                article = acn.articleCardNewsworthiness()
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
                article.show()


        # # Scroll up
        # st.markdown("[Scroll back to the top of page.](#arxiv-news-discovery-engine)")
        # add the link at the bottom of each page
        st.markdown(
            "<h5 style='text-align: center'><a href='#arxiv-news-discovery-engine'>Scroll back to the top of page.</a></h5>", unsafe_allow_html=True)

        # # Setup the bottom pagination
        # bottom_pages_container = st.container()
        # with bottom_pages_container:
        #     # Make columns for the pagination buttons - do I want to re-align this???
        #     _, col4, col5, col6, _ = st.columns([0.1, 0.1, 0.17, 0.1, 0.1])
        #     # Next page button if there's pages left
        #     if st.session_state.page+1 < max_pages:
        #         col6.button(">", on_click=next_page, key="next_bottom")
        #     # Emppty space if there's no next pages left
        #     else:
        #         col6.write("")  # this makes the empty column show up on mobile

        #     # Previous page button if there's pages left
        #     if st.session_state.page > 0:
        #         col4.button("<", on_click=prev_page, key="prev_bottom")
        #     # Empty space if there's no previous pages left
        #     else:
        #         col4.write("")  # this makes the empty column show up on mobile
        #     # Current page number
        #     col5.write(f"Page {1+st.session_state.page} of {max_pages}")
        #     # Scroll up
        #     st.markdown("[Scroll results back to the top.](#arxiv-news-discovery-engine)")
    
    else:
        st.write("No results found matching these filters.")
    #     article_cards.append(article)

    # # Display articles
    # for article in article_cards:
    #     article.show()

        


