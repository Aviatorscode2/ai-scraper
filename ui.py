import streamlit as st
import pathlib
from main import scrape_website, extract_body_content, clean_body_content, split_dom_content
from llm import parse_with_ollama

# function to load css from the assets folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load the external CSS
css_path = pathlib.Path("assets/style.css")
if css_path.exists():
    load_css(css_path)

st.title("AI Scraper")

st.markdown(
    "Enter a website URL to scrape, clean the text content, and display the result in smaller chunks."
)

url = st.text_input(label= "", placeholder="Enter the URL of the website you want to scrape")

if st.button("Scrape", key="scrape_button"):
    if url:
        try:
            # Step 1: Scrape the raw HTML content
            st.info("Scraping the website...")
            html_content = scrape_website(url)

            # Step 2: Extract the <body> content
            st.info("Extracting <body> content...")
            body_content = extract_body_content(html_content)

            # Step 3: Clean the body content
            st.info("Cleaning the extracted content...")
            cleaned_content = clean_body_content(body_content)

            # Step 4: Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Step 5: Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid website URL.")

# Step 2: Ask Questions About the DOM Content
# if "dom_content" in st.session_state:
#     parse_description = st.text_area("I am ready to provide insight to your scrape data.")

#     if st.button("Parse Content", key="parse_button"):
#         if parse_description.strip() and st.session_state.get("dom_content"):
#             st.info("Parsing the content...")
#             dom_chunks = split_dom_content(st.session_state.dom_content)
#             parsed_result = parse_with_ollama(dom_chunks, parse_description)
#             st.text_area("Parsed Results", parsed_result, height=300)
#         else:
#             st.error("Please provide valid DOM content and a description to parse.")