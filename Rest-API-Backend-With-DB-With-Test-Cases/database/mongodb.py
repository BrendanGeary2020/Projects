from pymongo import MongoClient
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")


# Connect to MongoDB
client = MongoClient(MONGODB_URI)

db = client[MONGODB_DATABASE]


# Collections
admins_collection = db["admins"]
customers_collection = db["customers"]


# Test MongoDB connection
try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)