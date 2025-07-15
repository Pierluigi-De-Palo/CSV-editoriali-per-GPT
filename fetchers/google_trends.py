import pandas as pd
from pytrends.request import TrendReq

def fetch_trends(keywords, timeframe='now 7-d', chunk_size=5):
    """
    Restituisce un DataFrame con la serie storica di interesse
    per ogni keyword. Google Trends supporta max 5 keyword per richiesta,
    quindi dividiamo in chunk di lunghezza chunk_size.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    df_total = None

    for i in range(0, len(keywords), chunk_size):
        chunk = keywords[i:i + chunk_size]
        pytrends.build_payload(chunk, timeframe=timeframe)
        df_chunk = pytrends.interest_over_time().drop(columns=['isPartial'])
        df_chunk = df_chunk.reset_index()               # porta 'date' da index a colonna
        df_chunk = df_chunk[['date'] + chunk]           # mantieni solo le colonne che ti servono

        if df_total is None:
            df_total = df_chunk
        else:
            df_total = pd.merge(df_total, df_chunk, on='date', how='outer')

    return df_total
