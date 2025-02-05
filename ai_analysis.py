import openai
# Carica la chiave API da variabile d'ambiente
#openai.api_key = os.getenv("OPENAI_API_KEY")
import streamlit as st

# Accedere alla chiave API dal file secrets.toml
openai_client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#st.write(f"La tua chiave API è: {openai_api_key}")
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
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un esperto analista finanziario."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
