import os 
import sys
import pymongo
import certifi 

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB 
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    -----------
    Client: MongoDB Client
        A shared MongoDB instance for the class 
    database: Database
        The specified database instance that MongoDBClient connects to.

    Methods:
    ----------
    __init__(database_name: str)->None
        Initializes the MongoDB connection using the given database name.
    """

    client = None # Shared MongoDBClient instance across all MongoDBClient Instances

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to MongoDB database. If no existing connection found, it establishes a new one

        parameters:
        -------------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        --------
        MyException
            If there is an issue connecting to MongoDB or if environment variable for MongoDB Url is not set.
        """
        try:
            # Check if MongoDB Client connection has already been established; if not, create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) # Retrieve MongoDB URL key from environment variables
                if mongo_db_url is None:
                    raise Exception(f"Environment Variable '{MONGODB_URL_KEY}' is not set")
                
                # Establish a connection 
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            # Use the shared MongoDB Client for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name] # connect to specified database
            self.database_name = database_name
            logging.info("MongoDB connection successful")

        except Exception as e:
            # Raise a custom Exception with traceback details if connection fails
            raise MyException(e,sys)