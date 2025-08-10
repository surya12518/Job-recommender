from scraper import scrape_remoteok
from embeddings import create_vector_index

search_term = input("Enter job keyword (default: data): ").strip() or "data"
df = scrape_remoteok(search_term, output_path="data/jobs.csv")
create_vector_index(df)
print("✅ Vector DB built successfully.")
