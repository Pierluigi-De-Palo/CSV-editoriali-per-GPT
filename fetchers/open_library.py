import requests
import pandas as pd

def fetch_openlib_subject(subject):
    """
    Recupera da OpenLibrary il numero di opere sotto il subject indicato.
    """
    key = subject.replace(" ", "_")
    url = f"https://openlibrary.org/subjects/{key}.json?limit=1"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    return pd.DataFrame([{
        "subject": subject,
        "work_count": data.get("work_count", 0)
    }])
