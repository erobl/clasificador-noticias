from abc import ABC, abstractmethod

class Connector(ABC):
    @abstractmethod
    def getemptynews(self):
        pass

    @abstractmethod
    def getallnews(self):
        pass

    @abstractmethod
    def inserttext(self, iid, text):
        pass

    @abstractmethod
    def getunclassifiednews(self):
        pass

    @abstractmethod
    def classifynews(self, iid, classobj, text=None):
        pass
