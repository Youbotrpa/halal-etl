import os
import requests
import yfinance as yf
from supabase import create_client, Client

# Récupère les infos d'environnement
SUPA_URL = os.environ.get('SUPA_URL')
SUPA_KEY = os.environ.get('SUPA_KEY')

# Connecte à Supabase
supabase: Client = create_client(SUPA_URL, SUPA_KEY)

# Récupère la liste des tickers depuis la table "instruments"
rows = supabase.table('instruments').select('ticker').execute()
tickers = [row['ticker'] for row in rows.data]

for t in tickers:
    data = yf.Ticker(t).history(period="1d")
    if not data.empty:
        last_close = float(data['Close'].iloc[-1])
        # Met à jour/insère dans la table 'prices_latest'
        supabase.table('prices_latest').upsert({'ticker': t, 'last_close': last_close}).execute()
        print(f"{t}: {last_close}")
    else:
        print(f"{t}: pas de données trouvées")
add daily_etl.py
