from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import numpy as np
import logging
import heapq
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
DATA_DIRECTORY = 'data/'
MODEL_DIRECTORY = 'models/'

def load_data():
    with open(DATA_DIRECTORY + 'metadata_corpus.pkl', 'rb') as f:
        metadata = pickle.load(f)
    return metadata['q_tok'], metadata['a_tok']


def build_w2v_model(qtokenized, atokenized, size=256, window=8, min_count=0, iter=500, name='model_vk_tg'):
    w2v_model = Word2Vec(qtokenized + atokenized, size=size, window=window, min_count=min_count, iter=iter)
    w2v_model.save(name)
    return w2v_model


def load_w2v_model(name='model_vk_tg'):
    return Word2Vec.load(MODEL_DIRECTORY + name)


def load_names(name='names.pkl'):
    with open(DATA_DIRECTORY + name, 'rb') as f:
        names = pickle.load(f)
    return names


def find_vector(model, message):
    vector = np.zeros(model.wv.vector_size)
    for word in message:
        if word in model.wv.vocab:
            vector = vector + model.wv[word]
    return vector


def vectorize_pairs(qtokenized, atokenized, model):
    # pairs = [(find_vector(model, q_tok), ' '.join(a_tok).strip()) for (q_tok, a_tok) in zip(qtokenized, atokenized)]
    names = load_names()
    pairs = [(find_vector(model, q_tok), replace_name(names, a_tok).strip()) for (q_tok, a_tok) in zip(qtokenized, atokenized)]
    return pairs


def replace_name(names, sent):
    answ = ""
    for word in sent:
        if word.lower() in names:
            word = word[0].upper() + '.'
        answ += word + ' '
    return answ


class Mes2Vec():
    def __init__(self):
        self.qtokenized, self.atokenized = load_data()
        self.w2v_model = load_w2v_model()
        self.pairs = vectorize_pairs(self.qtokenized, self.atokenized, self.w2v_model)
        self.names = load_names()

    def n_most_similar(self, message, n):
        vector = find_vector(self.w2v_model, message)
        heap = []
        for (v, s) in self.pairs:
            sim = cosine(v, vector)
            heapq.heappush(heap, (sim, s))
        return heap[:n]

    def replace_name(self, sent):
        answ = ""
        for word in sent:
            if word.lower() in self.names:
                word = word[0].upper() + '.'
            answ += word + ' '
        return answ

    def throw_sentence(self, message, n=5):
        sents = self.n_most_similar(message,n)
        # return ' '.join(np.random.choice([s[1] for s in sents], 1, [s[0] for s in sents])).strip()
        return np.random.choice([s[1] for s in sents], 1, [s[0] for s in sents])[0]

    def testing(self, samples=None):
        if samples == None:
            samples = ['привет как дела?', 'го встретимся?', 'надо делать курсач', 'как же не хочется учиться',
                       'надо идти гулять с ластоном']
        answeres = [self.throw_sentence(sample.split()) for sample in samples]
        return answeres
