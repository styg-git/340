from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'Chunk1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30061
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    # create method
    def create(self, data):
        # ensures entry is not empty
        if data is None:
            raise Exception("Nothing to save. Data parameter is empty.")

        # dictionary type checking
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")

        # insert a new document
        result = self.database.animals.insert_one(data)

        # return True for successful inserts, otherwise return False
        if result.inserted_id is not None:
            return True
        else:
            return False

    # read method
    def read(self, query):
        if query is None:
            raise Exception("Nothing to read. Data parameter is empty")

        # dictionary type checking
        if not isinstance(query, dict):
            raise TypeError("Data must be a dictionary.")

        # search for query match
        cursor = self.database.animals.find(query)
        # convert cursor to list
        result = list(cursor)
        return result

    # update method
    def update(self, query, new_info):
        if query is None or new_info is None:
            raise Exception("Query and update parameters cannot be empty.")

        if not isinstance(query, dict) or not isinstance(new_info, dict):
            raise TypeError("Query and update values must be dictionaries.")

        # First, find how many documents match the query
        match_count = self.database.animals.count_documents(query)

        if match_count == 1:
            # If exactly one document matches, update it
            result = self.database.animals.update_one(query, {"$set": new_info})
        elif match_count > 1:
            # If more than one document matches, update all of them
            result = self.database.animals.update_many(query, {"$set": new_info})
        else:
            # No matching documents
            raise Exception("No documents matched the query for update.")

        return result.modified_count

    # delete method
    def delete(self, to_delete):
        if to_delete is None:
            raise Exception("Nothing to delete. Data parameter is empty.")

        # dictionary type checking
        if not isinstance(to_delete, dict):
            raise TypeError("Delete information must be a dictionary.")

        # delete the document
        result = self.database.animals.delete_one(to_delete)

        # return number of deleted documents
        return result.deleted_count


