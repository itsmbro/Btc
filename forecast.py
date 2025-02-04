import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

def predict_prices(df, days=7):
    """Prevede i prezzi futuri usando ARIMA con parametri ottimizzati."""

    # Prendiamo solo la colonna 'Close' per la previsione
    data = df['Close'].dropna()

    # Trova automaticamente i migliori parametri ARIMA
    model_auto = auto_arima(data, seasonal=False, trace=True, suppress_warnings=True)
    best_order = model_auto.order  # Ottieni l'ordine ottimale (p, d, q)
    print(f"📊 Miglior ordine ARIMA trovato: {best_order}")

    # Creiamo e addestriamo il modello ARIMA con i parametri ottimizzati
    model = ARIMA(data, order=best_order)  
    model_fit = model.fit()

    # Facciamo la previsione per 'days' giorni
    forecast = model_fit.forecast(steps=days)

    # Creiamo un DataFrame con le date future
    future_dates = pd.date_range(start=df.index[-1], periods=days+1, freq='B')[1:]
    forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': forecast})
    
    return forecast_df
