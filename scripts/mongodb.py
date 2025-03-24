from pymongo import MongoClient


def load_data():
    # Replace with your MongoDB connection string
    CONNECTION_STRING = "mongodb://127.0.0.1:27018"  # For local MongoDB

    # Connect to the database and collection
    client = MongoClient(CONNECTION_STRING)
    db = client["archaeology_metadata"] # Database name
    collection = db["collection"] # Collection name

    return collection


