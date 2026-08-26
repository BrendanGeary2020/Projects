from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")


client = MongoClient(MONGODB_URI)

db = client[MONGODB_DATABASE]


# All users are stored in one collection.
# This allows MongoDB to enforce globally
# unique user IDs for both Admins and Customers.
users_collection = db["users"]

accounts_collection = db["accounts"]


try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)


# Prevent two users from having the same ID,
# regardless of whether they are an Admin or Customer.
users_collection.create_index(
    [("id", 1)],
    unique=True
)


# Prevent a customer from having more than one
# account of the same type.
accounts_collection.create_index(
    [("customer_id", 1), ("account_type", 1)],
    unique=True
)