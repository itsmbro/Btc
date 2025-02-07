import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from indicators import calculate_rsi, calculate_macd, calculate_sma, calculate_ema
from forecast import predict_prices  # Importiamo la funzione di previsione
from ml_forecast import predict_with_lightgbm


# Configura la pagina
st.set_page_config(page_title="💰easyFinance - by mickybi😏", layout="wide")

# Titolo e descrizione
st.title("📈 Smart Portfolio Manager")
st.markdown("Analizza il mercato azionario in tempo reale e gestisci il tuo portafoglio💰")



# Sidebar per la selezione del titolo
st.sidebar.header("Seleziona un asset")

# Liste separate per azioni e criptovalute
stocks = [
    'AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'META', 'NFLX', 'NVDA',  
    'AMD', 'INTC', 'BABA', 'V', 'JPM', 'DIS', 'PYPL', 'ADBE', 'CSCO', 'PEP', 'KO',  
    'NKE', 'PFE', 'MRNA', 'BA', 'XOM', 'T', 'IBM', 'ORCL', 'GE', 'UBER', 'SQ'  
]

cryptos = [
    'BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD',  
    'ADA-USD', 'DOGE-USD', 'DOT-USD', 'MATIC-USD', 'LTC-USD',  
    'AVAX-USD', 'LINK-USD', 'BCH-USD', 'XLM-USD', 'ATOM-USD'  
]

# Radio button per la scelta della categoria
asset_type = st.sidebar.radio("Tipo di asset", ["Azioni", "Criptovalute", "Altro"])

# Selezione del ticker
if asset_type == "Azioni":
    ticker = st.sidebar.selectbox("Seleziona un'azione", stocks + ["Altro..."])
elif asset_type == "Criptovalute":
    ticker = st.sidebar.selectbox("Seleziona una criptovaluta", cryptos + ["Altro..."])
else:
    ticker = "Altro..."

# Permetti input manuale se l'utente seleziona "Altro..."
if ticker == "Altro...":
    ticker = st.sidebar.text_input("Inserisci il simbolo dell'asset", "")






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
    # Calcola gli indicatori
    df = calculate_rsi(df)
    df = calculate_macd(df)
    df = calculate_sma(df)
    df = calculate_ema(df)

    # Creazione del grafico principale
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1, 
        row_heights=[0.7, 0.3],  
        subplot_titles=[f'Andamento di {ticker}', 'Indicatori Tecnici']
    )

    # Grafico candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    ), row=1, col=1)

    # Aggiunta indicatori tecnici
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='orange')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD', line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines', name='SMA', line=dict(color='green')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name='EMA', line=dict(color='red')), row=2, col=1)

    # Layout del grafico
    fig.update_layout(
        title=f"Andamento di {ticker}",
        xaxis_rangeslider_visible=False,
        height=700,
        legend=dict(x=0.5, y=1.1, xanchor='center', yanchor='bottom')
    )

    # Mostra il grafico
    st.plotly_chart(fig, use_container_width=True)

    # Mostra i risultati in tabella
    st.write("### Indicatori Tecnici")
    st.dataframe(df[['RSI', 'MACD', 'Signal', 'SMA', 'EMA']].tail())

    # Mostra dati storici
    st.write("### Dati Storici")
    st.dataframe(df)







# -------------------------------
# 🔥 SEZIONE PREVISIONE CON ARIMA
# -------------------------------
st.write("## 🔮 Previsione dei Prezzi")

# Selezione del periodo di previsione
days = st.slider("Seleziona il numero di giorni da prevedere", min_value=1, max_value=30, value=3)

# Bottone per ARIMA
if st.button("Genera Previsione (ARIMA)"):
    forecast_df = predict_prices(df, days)

    st.write(f"### Previsione per i prossimi {days} giorni (ARIMA)")
    st.dataframe(forecast_df)

    forecast_fig = go.Figure()

    forecast_fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Prezzo Storico', line=dict(color='blue')))
    forecast_fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Predicted Close"], mode='lines+markers', name='Previsione ARIMA', line=dict(color='red', dash='dash')))

    forecast_fig.update_layout(title="Previsione del Prezzo con ARIMA")
    st.plotly_chart(forecast_fig, use_container_width=True)

# Bottone per LightGBM
if st.button("Genera Previsione (LightGBM)"):
    forecast_df_lgbm = predict_with_lightgbm(df, days)

    st.write(f"### Previsione per i prossimi {days} giorni (LightGBM)")
    st.dataframe(forecast_df_lgbm)

    forecast_fig_lgbm = go.Figure()

    forecast_fig_lgbm.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Prezzo Storico', line=dict(color='blue')))
    forecast_fig_lgbm.add_trace(go.Scatter(x=forecast_df_lgbm["Date"], y=forecast_df_lgbm["Predicted Close"], mode='lines+markers', name='Previsione LightGBM', line=dict(color='green', dash='dot')))

    forecast_fig_lgbm.update_layout(title="Previsione del Prezzo con LightGBM")
    st.plotly_chart(forecast_fig_lgbm, use_container_width=True)










from ai_analysis import generate_market_comment  # Importa la funzione di analisi

# -------------------------------
# 🔥 SEZIONE ANALISI AI (GPT-4)
# -------------------------------
st.write("## 🤖 Analisi Automatica del Mercato")

if st.button("Genera Analisi AI"):
    with st.spinner("Generando il commento..."):
        ai_comment = generate_market_comment(ticker, df)
        st.write("### 📊 Commento AI")
        st.success(ai_comment)

