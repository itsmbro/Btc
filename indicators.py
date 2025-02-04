import pandas as pd

# Calcola l'RSI (Relative Strength Index)
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

# Calcola la MACD (Moving Average Convergence Divergence)
def calculate_macd(df, fast=12, slow=26, signal=9):
    df['EMA_fast'] = df['Close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    return df

# Calcola la Media Mobile Semplice (SMA)
def calculate_sma(df, period=20):
    df['SMA'] = df['Close'].rolling(window=period).mean()
    return df

# Calcola la Media Mobile Esponenziale (EMA)
def calculate_ema(df, period=20):
    df['EMA'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df
