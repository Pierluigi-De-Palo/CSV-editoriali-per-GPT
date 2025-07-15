import pandas as pd

from fetchers.google_trends import fetch_trends
from fetchers.google_books import fetch_books_metrics
from fetchers.open_library import fetch_openlib_subject

OUTPUT_FILE = "niches_enriched.csv"

def main():
    # 1) Leggi il CSV di partenza, colonna "Keyword principali"
    df = pd.read_csv("niches.csv")
    keywords = df["Keyword principali"].dropna().astype(str).tolist()

    # 2) Calcola volume di ricerca medio settimanale
    trends = fetch_trends(keywords)
    # prendi la media per ciascuna keyword
    avg_vol = trends[keywords].mean().rename("avg_search_volume")

    # 3) Recupera rating e recensioni da Google Books
    books = fetch_books_metrics("self publishing", max_results=20)
    avg_rating    = books["averageRating"].mean()
    total_reviews = books["ratingsCount"].sum()

    # 4) Recupera work_count da Open Library
    ol = fetch_openlib_subject("self publishing")
    work_count = ol["work_count"].iloc[0]

    # 5) Unisci al DataFrame originale
    df["avg_search_volume"] = df["Keyword principali"].map(avg_vol.to_dict())
    df["avg_rating"]        = avg_rating
    df["total_reviews"]     = total_reviews
    df["work_count"]        = work_count

    # 6) Calcola il rapporto sforzo/riuscita
    df["effort_success"] = (df["total_reviews"] * df["avg_rating"]) / df["avg_search_volume"]

    # 7) Esporta il CSV arricchito
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
