import os

MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://mongodb:27017/?replicaSet=rs0")
DATABASE_NAME = os.environ.get("MONGODB_APP_DB_NAME", "bookhub")
