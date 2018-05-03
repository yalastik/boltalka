import gensim
# from tqdm import tqdm_notebook
from gensim.models import Word2Vec
import logging
import string
from scipy.spatial.distance import cosine

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
FILE_NAME = '/media/yana/LENOVO/MyPyCharmPrj/boltalka/messages.txt'


def clear_messages(filename=FILE_NAME):
    with open(filename, 'r') as f:
        dialogs = f.read()
    messages = dialogs.split('\n')
    translator = str.maketrans('', '', string.punctuation)
    data = []
    for message in messages:
        data.append(message.translate(translator).lower().split())
    return data


def model(data, size=256, window=10, min_count=0, iter=100):
    model = Word2Vec(data, size=size, window=window, min_count=min_count, iter=iter)
    model.save('/media/yana/LENOVO/MyPyCharmPrj/boltalka/model2')
    return model


class Mess2Vec():
    def __init__(self, model, filename):
        self.w2v_model = model
        self.data = clear_messages(filename)
        self.vectors = {}

    def find_vector(self, message):
        if message not in self.vectors:
            vector = []
            for word in message:
                if word in self.w2v_model.wv.vocab:
                    vector += self.w2v_model.wv[word]
            self.vectors[message] = vector
        return self.vectors[message]

    def message_similarity(self, message1, message2):
        return 1 - cosine(self.find_vector(message1), self.find_vector(message2))


w2v_model = Word2Vec.load('/media/yana/LENOVO/MyPyCharmPrj/boltalka/model2')
m2v = Mess2Vec(w2v_model, FILE_NAME)
m2v.message_similarity('привет как дела'.split(), 'ну чо как оно'.split())
w2v_model.predict_output_word()
