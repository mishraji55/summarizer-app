from dotenv import load_dotenv
load_dotenv()
import os
import base64
import tempfile
import streamlit as st
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the summarization model
tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-248M")
base_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-248M")

# Function to extract text from a PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Get a page
        text += page.get_text()  # Extract text from the page
    if text.strip():
        return text
    return None

# Web Scraping Function
def scrape_article(url):
     response = requests.get(url, timeout=10)
     response.raise_for_status()  # Raise an error if the request fails
     soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content (common tags for articles)
     paragraphs = soup.find_all('p')
     article_text = "\n".join([para.get_text() for para in paragraphs])

     if not article_text.strip():
         raise ValueError("Unable to extract content from the page.")
     return article_text

# LLM pipeline for summarization
def llm_pipeline(input_text):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=500,
        min_length=50,
    )
    result = pipe_sum(input_text)
    return result[0]['summary_text']

@st.cache_data
# Function to display the PDF
def displayPDF(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit App
def main():
    st.title('AI Content Summarizer')

    # PDF Upload Section
    st.header("PDF content Summarizer")
    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])
    if uploaded_file is not None:
        if st.button("Summarize PDF"):
            col1, col2 = st.columns(2)

            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="/tmp/") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_filepath = temp_file.name

            with col1:
                st.info("Uploaded PDF File")
                displayPDF(temp_filepath)

            with col2:
                st.info("Summarization")
                input_text = extract_text_from_pdf(temp_filepath)
                if input_text:  # Proceed only if text extraction was successful
                    summary = llm_pipeline(input_text)
                    st.success(summary)
    st.header("Summarize Online Articles")
    url = st.text_input("Enter the URL of the article:")
    if st.button("Summarize Article"):
        if url.strip():
            st.info("Fetching and Summarizing Article...")
            article_text = scrape_article(url)
            if "Error:" in article_text:
                st.error(article_text)
            else: 
                col1, col2 = st.columns(2)
                with col1:
                    st.info("Original Article Content")
                    st.write(article_text[:1000] + "..." if len(article_text) > 1000 else article_text)
                with col2:
                    st.info("Summarized Content")
                    summary = llm_pipeline(article_text)
                    st.success(summary)
        else:
            st.warning("Please enter a valid URL.")

    # Text Input Section
    st.header("Summarize Your Text")
    user_input = st.text_area("Enter your content here:", height=200)
    if st.button("Summarize Text"):
        if user_input.strip():
            col1, col2 = st.columns(2)

            with col1:
                st.info("Original Content")
                st.write(user_input)

            with col2:
                st.info("Summarization")
                summary = llm_pipeline(user_input)
                st.success(summary)
        else:
            st.warning("Please enter some content to summarize.")

if __name__ == '__main__':
    main()
