import arxiv
import os
import ssl  # --- ADD THIS ---

# --- ADD THESE TWO LINES TO BYPASS THE SSL ERROR ---
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def download_research_papers(query, max_results=30):
    # Ensure the directory exists for your Librarian Agent
    save_dir = r"E:\Research Assistant\research_papers"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    print(f"🔎 Searching arXiv for: {query}...")
    
    # Search for papers
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    client = arxiv.Client()
    for result in client.results(search):
        # Format filename to be safe
        clean_title = "".join([c for c in result.title if c.isalnum() or c==' ']).rstrip()
        filename = f"{clean_title}.pdf"
        filepath = os.path.join(save_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"📥 Downloading: {result.title}...")
            result.download_pdf(dirpath=save_dir, filename=filename)
        else:
            print(f"✅ Already exists: {filename}")

if __name__ == "__main__":
    # Example: Fetch 5 papers about CNNs to populate your folder
    download_research_papers("Convolutional Neural Networks", max_results=30)