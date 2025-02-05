import openai

openai.api_key = "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"  # Sostituisci con la tua API Key

def generate_market_comment(ticker, df):
    """Genera un commento testuale sull'andamento del titolo azionario"""
    prezzi = df["Close"].tail(7).tolist()  # Ultimi 7 giorni di chiusura
    prompt = f"""
    Analizza l'andamento dell'azione {ticker} negli ultimi 7 giorni.
    I prezzi di chiusura sono: {prezzi}.
    Fornisci un'analisi dettagliata sui trend, la volatilità e possibili scenari futuri.
    """

    client = openai.OpenAI()  # Crea un client OpenAI

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
        )

    return response["choices"][0]["message"]["content"]
