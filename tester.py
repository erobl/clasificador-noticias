import text_classifier
import temas

tc = text_classifier.load("models/model.pkl")
tce = [text_classifier.load("models/model%d.pkl" % i) for i in range(len(temas.TEMASG))]

while True:
    val = input("Texto a ser probado: ")
    prediction = tc.predict([val])
    print("Predicción: %s" % temas.TEMASG[prediction[0]])
    proba = tc.predict_proba([val])[0,prediction[0]]
    print("Probabilidad: %0.2f" % proba)
    prediccion_especifica = tc.predict([val])
    print("Predicción específica: %s" % temas.TEMAS[prediccion_especifica[0]][prediccion_especifica[0]])
    proba = tc.predict_proba([val])[0,prediccion_especifica[0]]
    print("Probabilidad: %0.2f" % proba)
