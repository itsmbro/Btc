import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from indicators import calculate_rsi, calculate_macd, calculate_sma, calculate_ema
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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


    
    # Crea una figura con 2 pannelli: uno per i prezzi e uno per gli indicatori
fig = make_subplots(
    rows=2, cols=1, 
    shared_xaxes=True, 
    vertical_spacing=0.1, 
    row_heights=[0.7, 0.3],  # Imposta la proporzione tra i pannelli
    subplot_titles=[f'Andamento di {ticker}', 'RSI'],
    row_titles=['Prezzi', 'Indicatori']
)

# Grafico principale (candlestick)
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Candlestick"
), row=1, col=1)

# Aggiungi RSI come grafico a linee
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['RSI'],
    mode='lines',
    name='RSI',
    line=dict(color='orange')
), row=2, col=1)

# Aggiungi MACD, SMA, EMA se li vuoi visualizzare separatamente
fig.add_trace(go.Scatter(
    x=df.index,
    y=df['MACD'],
    mode='lines',
    name='MACD',
    line=dict(color='blue')
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['SMA'],
    mode='lines',
    name='SMA',
    line=dict(color='green')
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['EMA'],
    mode='lines',
    name='EMA',
    line=dict(color='red')
), row=2, col=1)

# Impostazioni generali del grafico
fig.update_layout(
    title=f"Andamento di {ticker}",
    xaxis_rangeslider_visible=False,
    height=700,  # Imposta l'altezza totale del grafico
)

# Mostra il grafico
st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    # Mostra dati in tabella
    st.write("### Dati Storici")
    st.dataframe(df)
else:
    st.error("Errore nel recupero dei dati. Verifica il simbolo inserito.")
