import os
import pandas as pd
import requests
from pytrends.request import TrendReq

OUTPUT_DIR = "output"

def fetch_trends(keywords):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, timeframe='now 7-d')
    df = pytrends.interest_over_time().reset_index().drop(columns=['isPartial'])
    return df

def fetch_books_metrics(subject, max_results=20):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"subject:{subject}",
        "printType": "books",
        "maxResults": max_results
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    rows = []
    for item in res.json().get("items", []):
        info = item.get("volumeInfo", {})
        rows.append({
            "title": info.get("title"),
            "averageRating": info.get("averageRating", 0),
            "ratingsCount": info.get("ratingsCount", 0)
        })
    return pd.DataFrame(rows)

def fetch_openlib_subject(subject):
    key = subject.replace(" ", "_")
    url = f"https://openlibrary.org/subjects/{key}.json?limit=1"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    return pd.DataFrame([{
        "subject": subject,
        "work_count": data.get("work_count", 0)
    }])

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    niches = pd.read_csv("niches.csv")
    keywords = niches["keyword"].dropna().tolist()

    trends_df = fetch_trends(keywords)
    trends_df.to_csv(f"{OUTPUT_DIR}/trends_selfpub.csv", index=False)

    books_df = fetch_books_metrics("self publishing", max_results=20)
    books_df.to_csv(f"{OUTPUT_DIR}/books_selfpub.csv", index=False)

    ol_df = fetch_openlib_subject("self publishing")
    ol_df.to_csv(f"{OUTPUT_DIR}/openlib_selfpub.csv", index=False)

    print("✅ Dati aggiornati in output/")

if __name__ == "__main__":
    main()
