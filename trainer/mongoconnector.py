from dbconnector import Connector
import pymongo

strings = {
    "full_text": "texto_completo",
    "classification_object": "autoclassification"
}

class MongoConnector(Connector):
    def __init__(self, url="mongodb://localhost:27017/", database="mediaNet", collection="posts_edgar2"):
        self.client = pymongo.MongoClient(url)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def getemptynews(self):
        return self.collection.find({"category": {"$exists": True},
                                     "subcategory": {"$exists": True},
                                     strings["full_text"]: {"$exists": False}})

    def getallnews(self):
        return self.collection.find({"category": {"$exists": True},
                                     "subcategory": {"$exists": True},
                                     strings["full_text"]: {"$exists": True}})

    def inserttext(self, iid, text):
        self.collection.find_one_and_update({"_id": iid},
                                            {"$set": {strings["full_text"]: text}})

    def getunclassifiednews(self):
        return self.collection.find({"category": {"$exists": False},
                                     "subcategory": {"$exists": False},
                                     strings["classification_object"]: {"$exists": False},
                                     "from.name": {"$in": ["Telenoticias", "La Nacion", "CR HOY", "Semanario Universidad"]}})

    def classifynews(self, iid, classobj, text=None):
        setobj = {}
        setobj[strings["classification_object"]] = classobj
        if text is not None:
            setobj[strings["full_text"]] = text
        self.collection.find_one_and_update({"_id": iid},
                                            {"$set": setobj})
