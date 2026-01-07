#FILE: matcher.py

from typing import List
import os

try:
    from sentence_transformers import SentenceTransformer, util
    MODEL_AVAILABLE = True
except Exception:
    MODEL_AVAILABLE = False

import math
import re

def simple_tokenize(text: str):
    text = text.lower()
    return re.findall(r"\b[a-z]{2,}\b", text)

class ResumeMatcher:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        if MODEL_AVAILABLE:
            try:
                self.model = SentenceTransformer(self.model_name)
            except Exception:
                self.model = None

    def embed(self, texts: List[str]):
        if self.model is not None:
            return self.model.encode(texts, convert_to_tensor=True)
        token_lists = [simple_tokenize(t) for t in texts]
        vocab = {}
        for tokens in token_lists:
            for t in tokens:
                if t not in vocab:
                    vocab[t] = len(vocab)
        vecs = []
        for tokens in token_lists:
            v = [0] * len(vocab)
            for t in tokens:
                v[vocab[t]] += 1
            vecs.append(v)
        return vecs

    def score_job_vs_resumes(self, job: str, resumes: List[str]) -> List[float]:
        docs = [job] + resumes
        embs = self.embed(docs)
        if MODEL_AVAILABLE and self.model is not None:
            job_emb = embs[0:1]
            resume_embs = embs[1:]
            sims = util.cos_sim(job_emb, resume_embs)[0]  # tensor
            return [float(x) for x in sims]
        def cosine(u, v):
            dot = sum(a*b for a,b in zip(u,v))
            nu = math.sqrt(sum(a*a for a in u))
            nv = math.sqrt(sum(b*b for b in v))
            return 0.0 if nu==0 or nv==0 else dot/(nu*nv)
        job_vec = embs[0]
        resume_vecs = embs[1:]
        return [cosine(job_vec, rv) for rv in resume_vecs]


