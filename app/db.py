from pymongo import MongoClient

from app.config import settings


def get_database():
    """Connects to elections database"""

    # Get host and port from settings
    user = settings["MONGO_USER"]
    password = settings["MONGO_PASSWORD"]
    host = settings["MONGO_HOST"]
    database = settings["MONGO_DATABASE"]

    # Provide the mongodb url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{user}:{password}@{host}"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client[f"{database}"]
