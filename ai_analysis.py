import openai
import os
from dotenv import load_dotenv

# Carica la chiave API da variabile d'ambiente
load_dotenv()
openai.api_key = os.getenv("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")

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
    response = openai.Completion.create(
        model="gpt-4",  # Usa GPT-4 per la generazione del testo
        prompt=prompt,
        max_tokens=300  # Impostazione del numero massimo di token da restituire
    )

    # Restituisci il commento generato
    return response.choices[0].text.strip()
