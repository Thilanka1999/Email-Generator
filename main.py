import os

os.environ["LD_LIBRARY_PATH"] = "/mount/src/Email-Generator/sqlite-amalgamation-3470000"

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from portfolio import Portfolio



def create_streamlit_app(llm, portfolio):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://rootcode.io/careers/data-scientist-1662542")
    submit_button = st.button("Submit")
    
    if submit_button:
        # try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            portfolio.load_portfolio()
            jobs = llm.extract_job(data)
            
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        # except Exception as e:
        #     st.error("An Error  Occurred: {e}")
            
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout='wide', page_title="cold email generator", page_icon="Dick")
    create_streamlit_app(chain, portfolio)
