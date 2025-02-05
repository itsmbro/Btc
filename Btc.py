import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from indicators import calculate_rsi, calculate_macd, calculate_sma, calculate_ema
from forecast import predict_prices  # Importiamo la funzione di previsione

# Configura la pagina
st.set_page_config(page_title="Smart Portfolio Manager", layout="wide")

# Titolo e descrizione
st.title("📈 Smart Portfolio Manager")
st.markdown("Analizza il mercato azionario in tempo reale e gestisci il tuo portafoglio.")

# Sidebar per la selezione del titolo
st.sidebar.header("Seleziona un'azione")
#ticker = st.sidebar.text_input("Inserisci il simbolo dell'azione (es. AAPL, TSLA)", "AAPL")




# Lista delle azioni più importanti
stock_list = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'META', 'NFLX', 'NVDA']

# Menu a discesa per scegliere un'azione o inserire manualmente il simbolo
ticker_choice = st.sidebar.selectbox("Scegli un'azione o inserisci un simbolo personalizzato", stock_list + ['Altro...'])

# Se l'utente seleziona 'Altro...', consenti l'inserimento manuale del simbolo
if ticker_choice == 'Altro...':
    ticker = st.sidebar.text_input("Inserisci il simbolo dell'azione (es. AAPL, TSLA)", "AAPL")
else:
    ticker = ticker_choice  # Usa il ticker selezionato dalla lista






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
    st.write("## 🔮 Previsione dei Prezzi con ARIMA")

    # Selezione del periodo di previsione
    days = st.slider("Seleziona il numero di giorni da prevedere", min_value=1, max_value=30, value=3)

    if st.button("Genera Previsione"):
        forecast_df = predict_prices(df, days)

        # Mostra la tabella con la previsione
        st.write(f"### Previsione per i prossimi {days} giorni")
        st.dataframe(forecast_df)

        # Grafico con i prezzi storici + previsione
        forecast_fig = go.Figure()

        # Prezzi storici
        forecast_fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode='lines',
            name='Prezzo Storico',
            line=dict(color='blue')
        ))

        # Prezzo previsto
        forecast_fig.add_trace(go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Predicted Close"],
            mode='lines+markers',
            name='Previsione',
            line=dict(color='red', dash='dash')
        ))

        forecast_fig.update_layout(title="Previsione del Prezzo con ARIMA")
        st.plotly_chart(forecast_fig, use_container_width=True)

else:
    st.error("Errore nel recupero dei dati. Verifica il simbolo inserito.")
