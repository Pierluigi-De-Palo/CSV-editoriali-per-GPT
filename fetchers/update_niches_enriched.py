import os
import pandas as pd

from fetchers.google_trends import fetch_trends
from fetchers.google_books import fetch_books_metrics
from fetchers.open_library import fetch_openlib_subject

OUTPUT_FILE = "niches_enriched.csv"

def main():
    # Leggi il CSV di partenza
    df = pd.read_csv("niches.csv")

    # 1) METRICA: volume di ricerca medio settimanale
    keywords = df["keyword"].dropna().tolist()
    trends = fetch_trends(keywords)
    # calcolo volume medio per ciascuna keyword
    avg_vol = trends[keywords].mean().rename("avg_search_volume")

    # 2) METRICA: rating medio e conteggio recensioni
    books = fetch_books_metrics("self publishing", max_results=20)
    # qui prendiamo il primo risultato come proxy di nicchia
    avg_rating     = books["averageRating"].mean()
    total_reviews  = books["ratingsCount"].sum()

    # 3) METRICA: dimensione catalogo
    ol = fetch_openlib_subject("self publishing")
    work_count = ol["work_count"].iloc[0]

    # 4) Calcolo “Effort-Success Ratio”
    #    esempio: (total_reviews * avg_rating) / avg_vol_media
    #    aggiungo la colonna al DF di partenza
    df["avg_search_volume"] = df["keyword"].map(avg_vol.to_dict())
    df["avg_rating"]        = avg_rating
    df["total_reviews"]     = total_reviews
    df["work_count"]        = work_count
    df["effort_success"]    = (total_reviews * avg_rating) / df["avg_search_volume"]

    # 5) Scrivi il CSV arricchito
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
