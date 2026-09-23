import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["bba_event_hub"]

events_collection = db["events"]
registrations_collection = db["registrations"]
messages_collection = db["messages"]

print("Connected to MongoDB successfully!")
