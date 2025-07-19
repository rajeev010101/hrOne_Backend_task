from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# Load values from .env
MONGO_URI = config("MONGO_URI")
DB_NAME = config("DB_NAME")

# Async MongoDB Client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

products_collection = db["products"]
orders_collection = db["orders"]
