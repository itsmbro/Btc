import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from modules.indicators import calculate_rsi, calculate_macd, calculate_sma, calculate_ema
# Configura la pagina
st.set_page_config(page_title="Smart Portfolio Manager", layout="wide")

# Titolo e descrizione
st.title("📈 Smart Portfolio Manager")
st.markdown("Analizza il mercato azionario in tempo reale e gestisci il tuo portafoglio.")

# Sidebar per la selezione del titolo
st.sidebar.header("Seleziona un'azione")
ticker = st.sidebar.text_input("Inserisci il simbolo dell'azione (es. AAPL, TSLA)", "AAPL")

# Funzione per ottenere dati di mercato
@st.cache_data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")
        return df
    except:
        return None

# Carica i dati
df = get_stock_data(ticker)

# Verifica se i dati sono validi
if df is not None and not df.empty:
    # Creazione del grafico con Plotly
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, 
        open=df["Open"], 
        high=df["High"], 
        low=df["Low"], 
        close=df["Close"], 
        name="Candlestick"
    ))

# Calcola gli indicatori
    df = calculate_rsi(df)
    df = calculate_macd(df)
    df = calculate_sma(df)
    df = calculate_ema(df)

# Mostra i risultati
    st.write("### Indicatori Tecnici")
    st.dataframe(df[['RSI', 'MACD', 'Signal', 'SMA', 'EMA']].tail())
    # Impostazioni del grafico
    fig.update_layout(title=f"Andamento di {ticker}", xaxis_rangeslider_visible=False)

    # Mostra il grafico
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostra dati in tabella
    st.write("### Dati Storici")
    st.dataframe(df)
else:
    st.error("Errore nel recupero dei dati. Verifica il simbolo inserito.")
