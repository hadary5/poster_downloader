import pymongo
class MongoDBDAL:
    def __init__(self):
        self.client= pymongo.MongoClient("localhost", 27017)
