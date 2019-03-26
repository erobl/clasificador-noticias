import argparse
from downloader import Downloader
from mongoconnector import MongoConnector
from collections import defaultdict
from streaming_classifier import StreamingClassifier
from text_classifier import tclassifier
import text_classifier
from itertools import tee
import temas
import numpy as np
import unidecode

parser = argparse.ArgumentParser(description="Entrena el modelo con la base de mongo.")

parser.add_argument("-d", dest="download", action="store_true")
parser.add_argument("-c", dest="classify", action="store_true")

args = parser.parse_args()

def download():
    print("downloading")
    mc = MongoConnector()
    d = Downloader()
    dd = defaultdict(int)
    for doc in mc.getemptynews():
        res = d.process(doc)
        dd[res.netloc] += 1
        print(dd)
        if res.text is not None:
            mc.inserttext(doc["_id"], res.text)

def tema_a_num(tema):
    try:
        return temas.temas_dic[tema.strip().lower()]
    except:
        print("Tema erróneo: %s" % (tema,))
        return -1

def temae_a_num(tema, i):
    try:
        return temas.temase_dics[i][unidecode.unidecode(tema.strip().lower())]
    except:
        # print("Tema erróneo: %s" % (tema,))
        return -1

def train():
    mc = MongoConnector()
    # will change to load dynamically later
    it = tee(mc.getallnews(), 3)
    categories = (tema_a_num(doc["category"]) for doc in it[0])
    subcategories = (temae_a_num(doc["subcategory"], tema_a_num(doc["category"])) for doc in it[1])
    text = (doc["texto_completo"] for doc in it[2])

    categories = np.asarray(list(categories))
    subcategories = np.asarray(list(subcategories))
    text = np.asarray(list(text))

    tc = tclassifier(name="General")
    tc.fit(text, categories)

    tc.save("models/model.pkl")

    # sc = StreamingClassifier(name="General")
    # sc.fit(text, categories, classes=range(len(temas.TEMASG)))
    # sc.save("models/model.pkl")

    for i in range(len(temas.TEMASG)):
        idx = (categories == i) & (subcategories >=0)
        X = text[idx]
        y = subcategories[idx]

        tc = tclassifier(name=temas.TEMASG[i])
        tc.fit(X, y)
        print("Precisión validacion cruzada para %s: %.02f, tipo de modelo: %s" % (temas.TEMASG[i], tc.score__, tc.classifier_type__))

        tc.save("models/model%d.pkl" % i)

def classify():
    model = text_classifier.load("models/model.pkl")
    models = [text_classifier.load("models/model%d.pkl" % i) for i in range(10)]
    mc = MongoConnector()
    d = Downloader()
    dd = defaultdict(int)
    for doc in mc.getunclassifiednews():
        if "texto_completo" in doc:
            text = doc["texto_completo"]
        else:
            res = d.process(doc)
            text = res.text

        if text is not None:
            resdoc = {}
            pred_cat = model.predict([text])[0]
            resdoc["general_prediction"] = temas.TEMASG[pred_cat]
            proba = list(model.predict_proba([text])[0])
            resdoc["general_proba"] = {}
            for tema, p in zip(temas.TEMASG, proba):
                resdoc["general_proba"][tema] = p
            pred_subcat = models[pred_cat].predict([text])[0]
            resdoc["specific_prediction"] = temas.TEMAS[pred_cat][pred_subcat]
            specific_proba = list(models[pred_cat].predict_proba([text])[0])
            resdoc["specific_proba"] = {}
            for clas, p in zip(models[pred_cat].classes_, specific_proba):
                c = temas.TEMAS[pred_cat][clas]
                resdoc["specific_proba"][c] = p

            mc.classifynews(doc["_id"], resdoc, text)

            dd[resdoc["general_prediction"]] += 1
            print(dd)


if(args.download):
    download()
elif(args.classify):
    print("classifying")
    classify()
else:
    print("training")
    train()
