# src/embeddings.py
import os
import asyncio
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load env variables
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

def create_vector_index(df, persist_dir="./chroma_db"):
    # Ensure event loop for Google API
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Prepare text chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = []
    for _, row in df.iterrows():
        content = f"{row['title']} at {row['company']} in {row['location']}\nApply here: {row['apply_url']}\n\n{row['description']} \n\nPosted on: {row['posted_date']}"
        chunks = text_splitter.split_text(content)
        docs.extend(chunks)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_texts(docs, embeddings, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

