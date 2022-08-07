import streamlit as st
from annotated_text import annotated_text

class articleCard():

    def __init__(self):

        self.arxiv_id = None
        self.title = None
        self.summary = None
        self.published = None
        self.arxiv_url = None
        self.arxiv_primary_category = None
        self.arxiv_all_categories = None
        self.code_mentioned = None
        self.readability = None
        self.completion1 = None
        self.completion2 = None
        self.completion3 = None
        self.predicted_newsworthiness = None
    
    def set_arxiv_id(self, arxiv_id):
        self.arxiv_id = arxiv_id
    
    def set_title(self, title):
        self.title = title
    
    def set_summary(self, summary):
        self.summary = summary
    
    def set_published(self, published):
        self.published = published
    
    def set_arxiv_url(self, arxiv_url):
        self.arxiv_url = arxiv_url
    
    def set_arxiv_primary_category(self, arxiv_primary_category):
        self.arxiv_primary_category = arxiv_primary_category
    
    def set_arxiv_all_categories(self, arxiv_all_categories):
        self.arxiv_all_categories = arxiv_all_categories
    
    def set_code_mentioned(self, code_mentioned):
        self.code_mentioned = code_mentioned
    
    def set_readability(self, readability):
        self.readability = readability
    
    def set_completion1(self, completion1):
        self.completion1 = completion1
    
    def set_completion2(self, completion2):
        self.completion2 = completion2
    
    def set_completion3(self, completion3):
        self.completion3 = completion3
    
    def set_predicted_newsworthiness(self, predicted_newsworthiness):
        self.predicted_newsworthiness = predicted_newsworthiness
    
    def show(self):

        '''Display the article card.'''

        # Make a container
        article_container = st.container()

        # Make columns
        main, aside = article_container.columns([4, 1])

        # Main column
        with main:
            # Title
            st.markdown(f"### {self.title}")
            # Published and link
            st.markdown(f"**Date Published**: {self.published} | [arXiv Link]({self.arxiv_url})")

            # Categories
            annotated_text(
                "**Categories**: ", 
                (self.arxiv_primary_category, "", "#afa"), 
                # " | All", 
                # self.arxiv_all_categories
            )
            

            # Summary
            st.markdown(f"{self.summary}")

            # Completion 1
            st.markdown(f"Completion 1: {self.completion1}")

            # Completion 2
            st.markdown(f"Completion 2: {self.completion2}")

            # Completion 3
            st.markdown(f"Completion 3: {self.completion3}")

        with aside: 
            annotated_text(
                "Newsworthiness:", 
                (f"{self.predicted_newsworthiness}", "#afa")
                )
            

        # # Code mentioned
        # st.markdown(f"Code mentioned: {self.code_mentioned}")

        # # Readability
        # st.markdown(f"Readability: {self.readability}")

        

        # # Predicted newsworthiness
        # st.markdown(f"Predicted newsworthiness: {self.predicted_newsworthiness}")

