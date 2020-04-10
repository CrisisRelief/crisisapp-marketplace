
from sklearn.metrics.pairwise import cosine_similarity
import textacy
import textacy.keyterms
from src.nlp.load_nlp_models import load_models
import numpy

class document_similarity(object):

    def __init__(self):
        self.lm = load_models()
        self.sent2vec = self.lm.load_sent2vec_model()
        return

    def get_sent2vec_similarity(self, src:str, tgt:str) -> numpy.float64:

        emb_src = self.sent2vec.embed_sentence(src.lower())
        emb_target = self.sent2vec.embed_sentence(tgt.lower())
        sim_score = cosine_similarity(emb_src.reshape(1,-1), emb_target.reshape(1,-1))
        score = sim_score[0][0]
        
        return score


