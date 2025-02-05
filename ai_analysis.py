import openai
import os
from dotenv import load_dotenv

# Carica la chiave API da variabile d'ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inizializza il client OpenAI
openai.api_key = api_key  # Imposta la chiave API globalmente

def generate_market_comment(ticker, df):
    """Genera un commento sull'andamento del mercato"""
    # Prendi gli ultimi 7 giorni di prezzi di chiusura
    prezzi = df["Close"].tail(7).tolist()
    
    # Costruisci il prompt per OpenAI
    prompt = f"""
    Analizza l'andamento dell'azione {ticker} negli ultimi 7 giorni.
    I prezzi di chiusura sono: {prezzi}.
    Fornisci un'analisi dettagliata sui trend, la volatilità e possibili scenari futuri.
    """
    
    # Chiamata API OpenAI per generare il commento
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Usa GPT-4 per la generazione del testo
        messages=[{"role": "user", "content": prompt}]
    )

    # Restituisci il commento generato
    return response.choices[0].message['content']
