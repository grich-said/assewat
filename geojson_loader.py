import pymongo
from pymongo import *

class GeoJsonLoaderNdvi():
    def __init__(self,url="mongodb://localhost:27017",dbname="assewat"):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[dbname]
        self.db["ndvi"].create_index([("geometry", "2dsphere")]);
        self.db["ndvi"].create_index([("ndvi.geometry", "2dsphere")])
        self.db["ndvi"].create_index('zone', unique=True)

    def inset(self,docs):
        for doc in docs:
            # Insert the document into the collection
            try:
                self.db["ndvi"].insert_one(doc)
            except pymongo.errors.DuplicateKeyError:
                # The document already exists, so update its "ndvi" list if the date is not already present
                existing_doc =  self.db["ndvi"].find_one({"zone": doc["zone"], "geometry": doc["geometry"]})
                for ndvi_new in doc["ndvi"]:
                    if ndvi_new["date"] not in [ndvi["date"] for ndvi in existing_doc["ndvi"]]:
                        self.db["ndvi"].update_one({"zone": doc["zone"], "geometry": doc["geometry"]},
                                              {"$push": {"ndvi": doc["ndvi"]}})
