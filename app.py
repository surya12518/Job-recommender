import os
import streamlit as st
from dotenv import load_dotenv
from src.scraper import scrape_remoteok
from src.embeddings import create_vector_index
from src.resume_parser import extract_text_from_pdf, parse_basic_resume
from src.rag_chain import build_rag_chain, recommend_jobs_from_profile

# Load env
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ GOOGLE_API_KEY not found in .env")
    st.stop()

st.title("AI Job Recommender")

# Upload resume
uploaded = st.file_uploader("Upload resume (pdf or txt)", type=['pdf', 'txt'])
profile = {}

if uploaded:
    with open("tmp_resume.pdf", "wb") as f:
        f.write(uploaded.getbuffer())
    text = extract_text_from_pdf("tmp_resume.pdf")
    profile = parse_basic_resume(text)
    st.write("Parsed profile:", profile)

# User inputs
skills = st.text_input("Add/override skills (comma separated)")
location = st.text_input("Preferred location")
job_search = st.text_input("Job keyword for scraping", value="data")
k = st.slider("How many job recommendations?", 1, 10, 5)

if st.button("Find jobs"):
    st.info(f"🔍 Scraping jobs for '{job_search}'...")
    df = scrape_remoteok(job_search, output_path="data/jobs.csv")
    st.success(f"✅ Scraped {len(df)} jobs.")

    st.info("⚙️ Building vector database...")
    vectordb = create_vector_index(df)
    st.success("✅ Vector database ready.")

    st.info("🤖 Generating recommendations...")
    qa = build_rag_chain(vectordb)
    summary = f"Skills: {skills or profile.get('skills')}; Location: {location}"
    result = recommend_jobs_from_profile(qa, summary, top_k=k)
    st.markdown(result)
    st.success("✅ Recommendations generated.")