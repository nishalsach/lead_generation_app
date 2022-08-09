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
        # self.arxiv_all_categories = None
        # self.code_mentioned = None
        # self.readability = None
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
    
    def set_published_hr(self, published_hr):
        self.published_hr = published_hr
    
    def set_arxiv_url(self, arxiv_url):
        self.arxiv_url = arxiv_url
    
    def set_arxiv_primary_category(self, arxiv_primary_category):
        self.arxiv_primary_category = arxiv_primary_category

    def set_arxiv_primary_category_hr(self, arxiv_primary_category_hr):
        self.arxiv_primary_category_hr = arxiv_primary_category_hr
    
    # def set_arxiv_all_categories(self, arxiv_all_categories):
    #     self.arxiv_all_categories = arxiv_all_categories
    
    # def set_code_mentioned(self, code_mentioned):
    #     self.code_mentioned = code_mentioned
    
    # def set_readability(self, readability):
    #     self.readability = readability
    
    def set_completion1(self, completion1):
        self.completion1 = completion1
    
    def set_completion2(self, completion2):
        self.completion2 = completion2
    
    def set_completion3(self, completion3):
        self.completion3 = completion3
    
    def set_predicted_newsworthiness(self, predicted_newsworthiness):
        self.predicted_newsworthiness = str(round(predicted_newsworthiness, 2)*100)[:2]+"/100"
    
    def show(self):

        '''Display the article card.'''

        # Make a container
        article_container = st.container()

        # Make columns
        main, aside = article_container.columns([4, 1])

        # Main column
        with main:

            # New containers
            header = st.container()
            summary = st.container()
            completions_container = st.container()

            with header:
                # Title
                st.subheader(f"{self.title}")
                # Published and link
                st.markdown(
                    f"**Date Published**: {self.published_hr}  \n **Primary Category**: {self.arxiv_primary_category_hr}")

            with summary:
                # Summary
                st.markdown(f"##### Summary  \n {self.summary}  \n [Link to full arXiv article.]({self.arxiv_url})")

            with completions_container:
                # Describe it
                st.markdown(f"##### Potential News Angles for framing this story:")
                # Completions
                st.markdown(f"1. {self.completion1}  \n 2. {self.completion2}  \n 3. {self.completion3}")

                # with tab1:
                #     st.write(self.completion1)
                # with tab2:
                #     st.write(self.completion2)
                # with tab3:
                #     st.write(self.completion3)
        
        # Aside column
        # with aside:
        #     st.markdown(f"Newsworthiness  \n ### {self.predicted_newsworthiness}")

        aside.metric(
            label="Newsworthiness", 
            value=self.predicted_newsworthiness)

        article_container.markdown("""---""")


        
        
