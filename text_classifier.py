import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
import pickle

from sklearn.model_selection import cross_val_score

# models
from sklearn.svm import SVC
"""
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
"""

class tclassifier():
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
        self.__model = None


    def fit(self, X_train, y_train):
        idf_train = self.__tfidf.fit_transform(X_train)
        best_score = 0
        best = None


        models = {
            "linear_svm": SVC(kernel="linear", probability=True)
        }

        for model in models:
            if model == "gaussian_nb":
                idf_train = idf_train.toarray()
            scores = cross_val_score(models[model], idf_train, y_train)
            score = sum(scores)/len(scores)
            # print("Classifier: %s at %.02f" % (model, score))
            if score > best_score:
                best_score = score
                best = model

        clean_models = {
            "linear_svm": SVC(kernel="linear", probability=True)
        }

        """
        clean_models = {
            "linear_svm": SVC(kernel="linear", probability=True),
            "sigmoid_svm": SVC(kernel="sigmoid", probability=True),
            "poly_svm": SVC(kernel="poly", probability=True),
            "svm": SVC(kernel="rbf", probability=True),
            "boost": GradientBoostingClassifier(),
            "sgd_hinge": SGDClassifier(),
            "sgd_perceptron": SGDClassifier(loss="perceptron"),
            "sgd_elastic": SGDClassifier(loss="log", penalty="elasticnet"),
            "neural_network": MLPClassifier(),
            "gaussian_nb": GaussianNB(),
            "bernoulli_nb": BernoulliNB(),
            "lasso": Lasso(),
            "knn": KNeighborsClassifier()
        }
        """

        self.score__ = best_score
        self.classifier_type__ = best

        self.__model = clean_models[model]
        self.__model.fit(idf_train, y_train)
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
