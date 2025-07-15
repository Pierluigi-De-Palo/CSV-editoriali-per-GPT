import os
import requests
import pandas as pd

# numero di libri da recuperare, modificabile tramite variabile d'ambiente
MAX_RESULTS = int(os.getenv('GB_MAX_RESULTS', 20))

def fetch_google_books(subject):
    """Restituisce titolo, rating medio e conteggio recensioni"""
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"subject:{subject}", "maxResults": MAX_RESULTS}
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    rows = []
    for item in res.json().get('items', []):
        info = item.get('volumeInfo', {})
        rows.append({
            'title': info.get('title'),
            'averageRating': info.get('averageRating', 0),
            'ratingsCount': info.get('ratingsCount', 0)
        })
    return pd.DataFrame(rows)
