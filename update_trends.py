import pandas as pd
from pytrends.request import TrendReq

# Connessione a Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

# Lista di keyword editoriali di base
keywords = ["coloring book", "kids story", "activity book", "early learning", "bedtime stories"]

# Build payload e ottieni trending search volume
pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='US', gprop='')

# Ottieni dati di interesse nel tempo
trends = pytrends.interest_over_time()

# Rinomina la colonna principale
trends = trends.drop(columns=["isPartial"])
trends = trends.mean().sort_values(ascending=False).reset_index()
trends.columns = ["Keyword", "Trend settimanale"]

# Carica CSV editoriale esistente
csv_path = "niches.csv"
df = pd.read_csv(csv_path)

# Per ogni keyword, aggiorna il campo "Trend settimanale aggiornato" se presente nella riga
for i, row in df.iterrows():
    for kw in keywords:
        if kw.lower() in str(row['Titolo']).lower():
            trend_val = trends[trends["Keyword"] == kw]["Trend settimanale"].values
            if trend_val.size > 0:
                df.at[i, "Trend settimanale aggiornato"] = trend_val[0]
                df.at[i, "Fonte trend"] = "Google Trends"

# Salva di nuovo il CSV aggiornato
df.to_csv(csv_path, index=False)
print("CSV aggiornato con i trend settimanali.")
