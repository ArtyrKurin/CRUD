import pymongo
from bson import ObjectId
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["CRUD"]
collection = db["Contacts"]
collection_companies = db["Companies"]

insertt = {
    "name": "Mx",
    "email": "mx.io",
    "Сотрудники": [
        {"_id": ObjectId('5e67850b91a15fd6742ebff4')},
        {"_id": ObjectId('5e67850b91a15fd6742ebff2')}
    ]
}

collection_companies.insert(insertt)
