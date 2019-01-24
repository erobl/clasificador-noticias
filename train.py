from text_classifier import tclassifier
import temas
import pandas as pd
from sklearn.model_selection import train_test_split

# load data (will change later)
import couchdb
couchdbserver = couchdb.Server()
db = couchdbserver["noticias2"]

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

X_train, X_test, y_train, y_test = train_test_split(noticias["texto"], noticias["ct"], random_state=0)

tc = tclassifier()
tc.fit(X_train, y_train)
print("Estimated accuracy: %.02f" % tc.score(X_test, y_test))

tc = tclassifier()
tc.fit(noticias["texto"], noticias["ct"])
tc.save("models/model.pkl")

# temas especificos
for i in range(len(temas.TEMASG)):
    tedf = noticias[noticias["ct"] == i]
    tedf["cte"] = tedf["tema"].apply(lambda x: temae_a_num(x,i))
    tedf = tedf[["cte","texto"]]
    tedf = tedf.dropna()
    tedf["cte"] = tedf["cte"].apply(int)
    X_train, X_test, y_train, y_test = train_test_split(tedf["texto"], tedf["cte"], random_state=0)

    tc = tclassifier()
    tc.fit(X_train, y_train)
    print("Estimated accuracy for %s: %.02f" % (temas.TEMASG[i], tc.score(X_test, y_test)))

    tc = tclassifier()
    tc.fit(tedf["texto"], tedf["cte"])
    tc.save("models/model%d.pkl" % i)

