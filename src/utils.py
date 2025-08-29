import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Cargar modelo de spaCy (asegúrate de instalarlo: python -m spacy download es_core_news_sm)
nlp = spacy.load("es_core_news_sm")

def preprocess(text: str) -> str:
    """Limpieza y lematización en español con spaCy."""
    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and not token.like_num
    ]
    return " ".join(tokens)

def load_data(path="data/Data_chatbot.csv") -> pd.DataFrame:
    """Carga el CSV con preguntas y respuestas."""
    df = pd.read_csv(path)
    if "Preguntas" not in df.columns or "Respuestas" not in df.columns:
        raise ValueError("El CSV debe tener columnas: 'Preguntas' y 'Respuestas'")
    return df

def vectorize(texts):
    """Crea representaciones TF-IDF."""
    vectorizer = TfidfVectorizer(preprocessor=preprocess, ngram_range=(1, 2), min_df=1)
    X = vectorizer.fit_transform(texts)
    return vectorizer, X
