from text_classifier import tclassifier
import temas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# load data (will change later)
import couchdb
couchdbserver = couchdb.Server()
db = couchdbserver["noticias2"]

# remove warnings (for now)
import warnings
warnings.filterwarnings("ignore")

CV = 10

def tema_a_num(tema):
    try:
        return temas.temas_dic[tema.strip().lower()]
    except:
        print("Tema erróneo: %s" % (tema,))
        return None

def temas_a_num(temass):
    ntemas = []
    for tema in temass:
        try:
            ntemas.append(temas.temas_dic[tema.strip().lower()])
        except Exception as e:
            print(e)
            print("Tema erróneo: %s" % (tema,))
            ntemas.append(None)

    return ntemas

def temae_a_num(tema, i):
    try:
        return temas.temase_dics[i][tema.strip().lower()]
    except:
        # print("Tema erróneo: %s" % (tema,))
        return None

def to_one_hot(i, dim):
    i = int(i)
    z = np.zeros((dim,))
    z[i] = 1
    return z

listnoticia = []
for doc in db.view("error/success"):
    listnoticia.append(doc["value"])
noticias = pd.DataFrame(listnoticia)
noticias["ct"] = noticias["temag"].apply(tema_a_num)

X = noticias["texto"]
y = noticias["ct"]
tc = tclassifier(name="General")
tc.fit(X, y)
print("Precisión validacion cruzada: %.02f, tipo de modelo: %s" % (tc.score__, tc.classifier_type__))

tc.save("models/model.pkl")

# temas especificos
for i in range(len(temas.TEMASG)):
    tedf = noticias[noticias["ct"] == i]
    tedf["cte"] = tedf["tema"].apply(lambda x: temae_a_num(x,i))
    tedf = tedf[["cte","texto"]]
    tedf = tedf.dropna()
    tedf["cte"] = tedf["cte"].apply(int)
    X = tedf["texto"]
    y = tedf["cte"]

    tc = tclassifier(name=temas.TEMASG[i])
    tc.fit(X, y)
    print("Precisión validacion cruzada para %s: %.02f, tipo de modelo: %s" % (temas.TEMASG[i], tc.score__, tc.classifier_type__))

    tc.save("models/model%d.pkl" % i)

