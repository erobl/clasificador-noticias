import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
import pickle

class tclassifier():
    def __init__(self, stop_words=None, sublinear_tf=True, min_df=5, norm="l2",
                 ngram_range=(1,2), strip_accents="unicode"):
        if stop_words is None:
            stop_words = stopwords.words("spanish")
        self.__tfidf = TfidfVectorizer(sublinear_tf=sublinear_tf, 
                                       min_df=min_df, norm=norm,
                                       encoding="utf-8", use_idf=True,
                                       ngram_range=ngram_range, 
                                       stop_words=stop_words,
                                       strip_accents=strip_accents)
        self.__model = SVC(kernel="linear", probability=True)

    def fit(self, X_train, y_train):
        idf_train = self.__tfidf.fit_transform(X_train)
        self.__model.fit(idf_train, y_train)
        return self

    def predict(self, X):
        idf = self.__tfidf.transform(X)
        return self.__model.predict(idf)

    def predict_proba(self, X):
        idf = self.__tfidf.transform(X)
        return self.__model.predict_proba(idf)

    def score(self, X, y):
        idf = self.__tfidf.transform(X)
        return self.__model.score(idf, y)

    def save(self, filename):
        with open(filename, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

def load(filename):
    with open(filename, "rb") as pickle_file:
        return pickle.load(pickle_file)
