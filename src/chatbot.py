import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_data, vectorize, preprocess

class Chatbot:
    def __init__(self, data_path="data/Data_chatbot.csv"):
        self.df = load_data(data_path)
        self.vectorizer, self.X = vectorize(self.df["Preguntas"].tolist())

    def get_response(self, user_input: str, threshold=0.3) -> str:
        """Devuelve la respuesta más adecuada según similitud coseno.
       Si la similitud máxima es menor a threshold, pide reformular."""
        user_vec = self.vectorizer.transform([preprocess(user_input)])
        similarities = cosine_similarity(user_vec, self.X)
        max_sim = np.max(similarities)
        if max_sim < threshold:
            return "No entendí tu pregunta, ¿puedes reformularla?"
        idx = np.argmax(similarities)
        return self.df["Respuestas"].iloc[idx]


    def suggest_questions(self, top_n=3):
        """Sugiere algunas preguntas que el usuario puede hacer."""
        return self.df["Preguntas"].sample(n=top_n).tolist()
