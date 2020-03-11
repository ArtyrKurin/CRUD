import pymongo
from bson import ObjectId
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["CRUD"]
collection = db["Contacts"]
collection_companies = db["Companies"]

f = collection_companies.find({})
key = '5e68f22c4696e451f49e8bc0'
print(collection_companies.find_one({'Сотрудники': {'_id': ObjectId('5e67850b91a15fd6742ebff2')}}))
