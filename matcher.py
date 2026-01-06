#FILE: matcher.py

from typing import List
import math
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


def simple_tokenize(text: str):
    text = text.lower()
    return re.findall(r"\b[a-z]{2,}\b", text)


class ResumeMatcher:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.documents = None

    def fit_transform(self, documents: List[str]):
        self.documents = documents
        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(documents)
            return self.tfidf_matrix
        vocab = {}
        tokenized = [simple_tokenize(d) for d in documents]
        for tokens in tokenized:
            for t in tokens:
                if t not in vocab:
                    vocab[t] = len(vocab)
        tf = []
        for tokens in tokenized:
            vec = [0] * len(vocab)
            for t in tokens:
                vec[vocab[t]] += 1
            tf.append(vec)
        N = len(tf)
        df = [0] * len(vocab)
        for vec in tf:
            for i, v in enumerate(vec):
                if v > 0:
                    df[i] += 1
        idf = [math.log((N + 1) / (d + 1)) + 1 for d in df]
        tfidf = [[v * i for v, i in zip(vec, idf)] for vec in tf]
        self.vectorizer = vocab
        return tfidf

    def similarity(self, a, b):
        if SKLEARN_AVAILABLE:
            return linear_kernel(a, b)
        def cosine(x, y):
            dot = sum(i * j for i, j in zip(x, y))
            nx = math.sqrt(sum(i * i for i in x))
            ny = math.sqrt(sum(j * j for j in y))
            return 0.0 if nx == 0 or ny == 0 else dot / (nx * ny)
        return [[cosine(x, y) for y in b] for x in a]


