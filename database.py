import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

print("MONGO_URI EXISTS:", bool(MONGO_URI))

if MONGO_URI:
    parsed = urlparse(MONGO_URI)
    print("MONGO USER:", parsed.username)
    print("MONGO HOST:", parsed.hostname)

client = MongoClient(MONGO_URI)

db = client["bba_event_hub"]

events_collection = db["events"]
registrations_collection = db["registrations"]
messages_collection = db["messages"]

try:
    client.admin.command("ping")
    print("MONGODB PING: SUCCESS")
except Exception as e:
    print("MONGODB PING ERROR:", e)
