from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

def build_rag_chain(vectordb, model_name="gemini-2.5-flash"):
    llm = ChatGoogleGenerativeAI(model=model_name)  # uses GOOGLE_API_KEY
    retriever = vectordb.as_retriever(search_kwargs={"k":5})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa

def recommend_jobs_from_profile(qa_chain, profile_summary, top_k=5):
    prompt = f"""You are a friendly career assistant. Given the candidate profile:
{profile_summary}

Retrieve and summarize the top {top_k} most relevant job postings. For each job, give:
- Job title & company & apply URL 
- Location
- Short 2-line fit explanation (why this matches the candidate)
- Suggested next action (apply/learn X)
Keep it concise."""
    resp = qa_chain.run(prompt)
    return resp
