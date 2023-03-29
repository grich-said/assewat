import pymongo
from pymongo import *

class GeoJsonLoaderNdvi():
    def __init__(self,url="mongodb://localhost:27017",dbname="assewat"):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[dbname]
        self.db["ndvi"].create_index([("geometry", "2dsphere")]);
        self.db["ndvi"].create_index([("ndvi.geometry", "2dsphere")])

    def insetOne(self,doc):
        self.db["ndvi"].insert_one(doc)
