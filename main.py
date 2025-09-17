import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_gemini   # ✅ changed from parse_with_ollama

st.title("AI Web Scraper with ollama")

url = st.text_input("Enter the URL to scrape:")

if st.button("Scrape"):
    if url.strip():
        st.write("Scraping the website...")
        html = scrape_website(url)
        body_content = extract_body_content(html)
        clean_content = clean_body_content(body_content)

        st.session_state.dom_content = clean_content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content", clean_content, height=300)
    else:
        st.warning("Please enter a valid URL before scraping.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("What do you want to parse from the DOM content?")

    if st.button("Parse"):
        if parse_description.strip():
            st.write("Parsing the DOM content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_gemini(dom_chunks, parse_description)  # ✅ updated function call
            st.subheader("Parsed Results")
            st.write(result)
        else:
            st.warning("Please enter a parsing description before parsing.")
