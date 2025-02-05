import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def predict_prices(df, days=7):
    """Prevede i prezzi futuri usando ARIMA con parametri fissi."""
    
    # Prendiamo solo la colonna 'Close' per la previsione
    data = df['Close'].dropna()

    # Creiamo e addestriamo il modello ARIMA (ordine p=3, d=1, q=0)
    model = ARIMA(data, order=(5,1,2))  # p=3, d=1, q=0
    model_fit = model.fit()

    # Facciamo la previsione per 'days' giorni
    forecast = model_fit.forecast(steps=days)

    # Creiamo un DataFrame con le date future
    future_dates = pd.date_range(start=df.index[-1], periods=days+1, freq='B')[1:]
    forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': forecast})
    
    return forecast_df
