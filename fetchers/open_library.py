import requests
import pandas as pd

def fetch_open_library(subject, top_n=5):
    """Restituisce work_count e top_n subjects"""
    key = subject.replace(' ', '_')
    url = f"https://openlibrary.org/subjects/{key}.json"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    work_count = data.get('work_count', 0)
    subjects = [s['name'] for s in data.get('subject', [])][:top_n]
    return pd.DataFrame([{
        'work_count': work_count,
        'top_subjects': ','.join(subjects)
    }])
