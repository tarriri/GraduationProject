from pymongo import MongoClient


class MongoDBAccessLayer:

    __fieldConnection = None

    def __get_connection(self):
        if self.__fieldConnection is None:
            self.__fieldConnection = MongoClient('localhost', 27017)
        return self.__fieldConnection

    @property
    def connection(self):
        return  self.__get_connection()

    def add_to_collection(self, collection_name, data):
        result = self.connection.NewsAnalysis[str(collection_name)].insert_one(data)
        return result
