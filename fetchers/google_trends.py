from pytrends.request import TrendReq
import pandas as pd

def fetch_trends(keywords, retries=3, timeout=(10,25)):
    """
    keywords: lista di keyword
    retries: tentativi in caso di errore
    timeout: (connect, read) in secondi
    """
    for attempt in range(1, retries+1):
        try:
            pytrends = TrendReq(hl='en-US', tz=360, retries=retries, backoff_factor=0.5)
            pytrends.build_payload(keywords, timeframe='now 7-d', timeout=timeout)
            df = pytrends.interest_over_time().reset_index().drop(columns=['isPartial'])
            return df
        except Exception as e:
            print(f"Tentativo {attempt} fallito: {e}")
    raise RuntimeError("Impossibile recuperare dati Google Trends")
