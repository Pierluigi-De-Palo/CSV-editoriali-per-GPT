import os
import pandas as pd

from fetchers.google_trends import fetch_trends
from fetchers.google_books import fetch_books_metrics
from fetchers.open_library import fetch_openlib_subject

OUTPUT_DIR = "output"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1) Leggi le tue keyword dalla colonna "Keyword principali"
    niches   = pd.read_csv("niches.csv")
    keywords = niches["Keyword principali"].dropna().astype(str).tolist()

    # 2) Google Trends (chunking automatico a 5 keyword per batch)
    trends_df = fetch_trends(keywords)
    trends_df.to_csv(f"{OUTPUT_DIR}/trends_selfpub.csv", index=False)

    # 3) Google Books - metriche base per "self publishing"
    books_df = fetch_books_metrics("self publishing", max_results=20)
    books_df.to_csv(f"{OUTPUT_DIR}/books_selfpub.csv", index=False)

    # 4) OpenLibrary - conteggio opere per "self publishing"
    ol_df = fetch_openlib_subject("self publishing")
    ol_df.to_csv(f"{OUTPUT_DIR}/openlib_selfpub.csv", index=False)

    print("✅ Dati self-publishing aggiornati in output/")

if __name__ == "__main__":
    main()
