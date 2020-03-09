import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["CRUD"]
collection = db["Contacts"]
collection_companies = db["Companies"]
