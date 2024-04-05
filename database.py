from pymongo import MongoClient

client = None
db = None
collection = None

def connect_to_mongodb(mongodb_url: str):
    global client, db, collection
    client = MongoClient(mongodb_url)
    db = client.get_database()
    collection = db.get_collection("students")
