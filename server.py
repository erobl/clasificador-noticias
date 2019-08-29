from multiprocessing import Process, Pipe
import text_classifier
import temas
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

# procesamos los datos en un hilo aparte
def thread(conn):
    general_model = text_classifier.load("models/model.pkl")
    models = [text_classifier.load("models/model%d.pkl" % i) for i in range(len(temas.TEMAS))]
    while True:
        text = conn.recv()
        prediction = int(general_model.predict([text])[0])
        proba = general_model.predict_proba([text])[0,:].tolist()
        prediction_specific = int(models[prediction].predict([text])[0])
        proba_specific = models[prediction].predict_proba([text])[0,:].tolist()
        conn.send({"general_class": prediction, "general_proba": proba,
                   "specific_class": models[prediction].classes_.tolist().index(prediction_specific),
                   "specific_proba": proba_specific,
                   "general_names": temas.TEMASG,
                   "specific_names": [temas.TEMAS[prediction][i] for i in models[prediction].classes_]})

class classifierThread():
    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()
        p = Process(target=thread, args=(self.child_conn,))
        p.start()

    def send_data(self, data):
        self.parent_conn.send(data)
        return self.parent_conn.recv()

ct = classifierThread()

app = Flask(__name__)

@app.route("/")
def tester():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    results = ct.send_data(data["text"])
    return jsonify(results)

if __name__ == '__main__':
   app.config['JSON_AS_ASCII'] = False
   app.run(debug = True)
