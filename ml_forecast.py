import pandas as pd

def predict_prices_custom(df, days=5):
    # Assicurati che ci siano le colonne necessarie
    data = df[['Close', 'Open', 'EMA_Fast', 'EMA_Slow']].dropna().copy()

    # Inizializza una lista per salvare le previsioni
    predictions = []

    # Prendi i valori iniziali dall'ultimo giorno disponibile
    last_close = data['Close'].iloc[-1]
    last_open = data['Open'].iloc[-1]
    last_ema_fast = data['EMA_Fast'].iloc[-1]
    last_ema_slow = data['EMA_Slow'].iloc[-1]

    for i in range(days):
        # Calcolo del prezzo futuro
        predicted_price = (
            0.05 * last_ema_fast 
            - 0.002 * last_ema_slow 
            + (last_close - last_open) 
            + last_close
        )

        # Salva la previsione
        predictions.append({
            'Day': i + 1,
            'Predicted Close': predicted_price
        })

        # Aggiorna i valori per il giorno successivo
        last_open = last_close  # Consideriamo il nuovo open uguale al close precedente
        last_close = predicted_price  

        # Aggiorna EMA usando la formula EMA = α * prezzo + (1 - α) * EMA_precedente
        alpha_fast = 2 / (10 + 1)  # EMA Fast con periodo 10
        alpha_slow = 2 / (20 + 1)  # EMA Slow con periodo 20

        last_ema_fast = alpha_fast * predicted_price + (1 - alpha_fast) * last_ema_fast
        last_ema_slow = alpha_slow * predicted_price + (1 - alpha_slow) * last_ema_slow

    return pd.DataFrame(predictions)

