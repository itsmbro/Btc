import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Funzione per recuperare i dati da CoinGecko API
def get_bitcoin_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '30',  # Modifica il numero di giorni per cambiare l'intervallo
        'interval': 'daily'  # Può essere 'daily', 'weekly', 'monthly'
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    # Estrai i prezzi da "prices" e convertili in un DataFrame
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    
    # Converti il timestamp in formato leggibile
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

# Titolo dell'app
st.title("📉 Andamento Prezzo Bitcoin")

# Descrizione dell'app
st.write("""
    Questa app mostra l'andamento del prezzo di Bitcoin negli ultimi 30 giorni.
    Puoi modificare l'intervallo temporale o la frequenza dei dati tramite le opzioni.
""")

# Seleziona l'intervallo temporale
days = st.slider('Seleziona l\'intervallo di giorni per l\'analisi:', 1, 365, 30)
interval = st.selectbox('Seleziona l\'intervallo di dati:', ['daily', 'weekly', 'monthly'])

# Ottieni i dati di Bitcoin
st.write("Caricamento dei dati...")
df = get_bitcoin_data()

# Visualizza i dati su un grafico
st.write(f"Andamento del prezzo di Bitcoin negli ultimi {days} giorni:")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['timestamp'], df['price'], label='Prezzo di Bitcoin', color='orange')
ax.set_title('Andamento del prezzo di Bitcoin (USD)')
ax.set_xlabel('Data')
ax.set_ylabel('Prezzo in USD')
ax.grid(True)
st.pyplot(fig)
