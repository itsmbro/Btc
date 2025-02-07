import pandas as pd

# Funzione per la previsione basata sulla formula personalizzata
def predict_prices_custom(df, days=5):
    forecast = []
    last_close = df['Close'].iloc[-1]
    last_open = df['Open'].iloc[-1]
    ema_fast = df['EMA'].iloc[-1]  # Assumiamo che EMA calcolato sia EMA_fast
    ema_slow = df['EMA'].rolling(window=20).mean().iloc[-1]  # Media mobile più lenta

    for i in range(days):
        price_change = last_close - last_open
        predicted_price = 0.05 * ema_fast - 0.002 * ema_slow + price_change + last_close

        # Aggiungiamo il risultato alla lista delle previsioni
        forecast.append({
            'Day': i + 1,
            'Predicted Close': predicted_price
        })

        # Aggiorniamo i valori per il giorno successivo
        last_open = last_close  # Il nuovo "open" sarà il "close" precedente
        last_close = predicted_price
        ema_fast = (ema_fast * 0.9) + (predicted_price * 0.1)  # Simulazione semplice per aggiornare EMA_fast
        ema_slow = (ema_slow * 0.95) + (predicted_price * 0.05)  # Simulazione per EMA_slow

    forecast_df = pd.DataFrame(forecast)
    return forecast_df

