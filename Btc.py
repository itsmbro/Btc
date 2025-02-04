import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Funzione per ottenere i dati di Bitcoin dalla API di CoinGecko
def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",  # Ultimi 30 giorni
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    return prices

# Funzione per fare una previsione del prezzo di Bitcoin
def predict_price(prices):
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['day'] = (df['date'] - df['date'].min()).dt.days  # Numero di giorni dall'inizio
    X = df[['day']]  # Feature: giorni dall'inizio
    y = df['price']  # Target: prezzo di Bitcoin
    model = LinearRegression()
    model.fit(X, y)
    
    # Previsione del prossimo giorno (giorno successivo)
    next_day = np.array([[df['day'].max() + 1]])
    predicted_price = model.predict(next_day)
    return df, predicted_price[0]

# Titolo dell'app
st.title("🔮 Previsione del Prezzo di Bitcoin")

# Recupera i dati di Bitcoin
st.write("Caricando i dati di Bitcoin...")
prices = get_bitcoin_data()

# Mostra il grafico del prezzo di Bitcoin negli ultimi 30 giorni
st.write("Grafico del prezzo di Bitcoin negli ultimi 30 giorni:")
df, predicted_price = predict_price(prices)

# Crea il grafico
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['date'], df['price'], label="Prezzo storico di Bitcoin", color='blue')
ax.set_xlabel('Data')
ax.set_ylabel('Prezzo (USD)')
ax.set_title('Bitcoin: Prezzo negli ultimi 30 giorni')
ax.legend()
st.pyplot(fig)

# Mostra la previsione del prezzo per il prossimo giorno
st.write(f"### Previsione del prezzo di Bitcoin per il prossimo giorno:")
st.write(f"Il prezzo previsto di Bitcoin sarà di **${predicted_price:.2f}**")
