import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import pickle


# tfidfvectorizer replacement
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from itertools import tee, zip_longest
from gensim.parsing.preprocessing import strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_numeric, remove_stopwords, stem_text, preprocess_string
from gensim.matutils import sparse2full
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

# models
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
"""
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
"""

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class StreamingClassifier():
    def __init__(self, stop_words=stopwords.words("spanish"), 
                 sublinear_tf=True, min_df=5, norm="l2", ngram_range=(1,2), 
                 strip_accents="unicode", name=None):
        self.name = name
        self.__tfidf = TfidfVectorizer(sublinear_tf=sublinear_tf, 
                                       min_df=min_df, norm=norm,
                                       encoding="utf-8", 
                                       ngram_range=ngram_range, 
                                       stop_words=stop_words,
                                       strip_accents=strip_accents)

        def remove_stopwords(s):
            return " ".join(w for w in s.split() if w not in stop_words)

        def stem_text(text):
            s = SnowballStemmer("spanish")
            return ' '.join(s.stem(word) for word in text.split())

        self.__FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation,
                          strip_multiple_whitespaces, strip_numeric,
                          remove_stopwords, stem_text]
        self.__dictionary = Dictionary()
        self.__tfidf = None
        self.__model = SGDClassifier() # SVC(kernel="linear", probability=True)


    def fit(self, texts, ys, classes, block_size=4):
        docs = (preprocess_string(text, self.__FILTERS) for text in texts)
        docs1, docs2 = tee(docs, 2)
        self.__dictionary.add_documents(docs1)
        bow = (self.__dictionary.doc2bow(doc) for doc in docs2)
        bow1, bow2 = tee(bow, 2)
        self.__tfidf = TfidfModel(bow1)
        idfs = (self.__tfidf[ws] for ws in bow2)
        idfvecs = (sparse2full(idf, self.__dictionary.num_pos) for idf in idfs)

        for g in grouper(zip(idfvecs, ys), block_size):
            idf = []
            y = []
            for tup in g:
                if tup is not None:
                    idf.append(tup[0])
                    y.append(tup[1])
            idf, y = np.asarray(idf), np.asarray(y)
            self.__model.partial_fit(idf, y, classes=classes)

        self.classes_ = self.__model.classes_
        return self

    def predict(self, X):
        if self.__model is not None:
            idf = self.__tfidf.transform(X)
            idf = idf.toarray()
            return self.__model.predict(idf)
        else:
            return None

    def predict_proba(self, X):
        if self.__model is not None:
            idf = self.__tfidf.transform(X)
            idf = idf.toarray()
            return self.__model.predict_proba(idf)
        else:
            return None

    def score(self, X, y):
        if self.__model is not None:
            idf = self.__tfidf.transform(X)
            idf = idf.toarray()
            return self.__model.score(idf, y)
        else:
            return None

    def save(self, filename):
        with open(filename, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def get_params(self, deep=True):
        return { "model": self.__model.get_params(deep=deep),
                "vectorizer": self.__tfidf.get_params(deep=deep) }

    def set_params(self, model, vectorizer):
        self.__tfidf.set_params(vectorizer)
        self.__model.set_params(model)

def load(filename):
    with open(filename, "rb") as pickle_file:
        return pickle.load(pickle_file)
