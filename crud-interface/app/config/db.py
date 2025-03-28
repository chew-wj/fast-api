import os
from pymongo import MongoClient

# Read MongoDB URI, username, and password from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

# Ensure the URI, username, and password are set
if not all([MONGODB_URI, MONGODB_USERNAME, MONGODB_PASSWORD]):
    raise ValueError("MongoDB credentials are missing!")

# Format MongoDB URI using the username and password from secrets
MONGO_CONNECTION_STRING = MONGODB_URI.replace("<username>", MONGODB_USERNAME).replace("<password>", MONGODB_PASSWORD)

# Connect to MongoDB
conn = MongoClient(MONGO_CONNECTION_STRING)


