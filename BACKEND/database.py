from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["getyourseat"]

users_collection = db["users"]
events_collection = db["events"]
bookings_collection = db["bookings"]