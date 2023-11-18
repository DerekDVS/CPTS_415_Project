import json  # json statements
import pymongo
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://AmazonDB:Password@cluster0.sip4gxt.mongodb.net/"
DATABASE_NAME = "AmazonDB"
DATA_COLLECTION_NAME = "AmazonDB"
REVIEW_COLLECTION_NAME = "ReviewAmazonDB"

class Database_Manager:
    def __init__(self):
        try:
            self.client = MongoClient(CONNECTION_STRING)
            self.db = self.client[DATABASE_NAME]
            self.db.command("ping")
            print(f"Connected to MongoDB database: {DATABASE_NAME}")

        except Exception as e:
            print("Error connecting to MongoDB:", str(e))

    def search_data(self, id=None, asin=None, title=None, group=None, salesrank=None):
        """
            Searches the table book

            :param conn: The connection
            :return: None
        """
        collection = self.db[DATA_COLLECTION_NAME]
        
        
        query = {}
        
        if id: query["Id"] = id
        if asin: query["ASIN"] = id
        if title: query["title"] = title
        if group: query["group"] = group
        if salesrank: query["salesrank"] = salesrank
        result = collection.find(query)

        for document in result:
            var = (document["Id"], document["ASIN"], document["title"], document["group"], document["salesrank"])
            print(var)
        
        return query, result

    def search_reviews(self, id=None, total=None, downloaded=None, avg_rating=None, reviews=None):
        collection = self.db[REVIEW_COLLECTION_NAME]

        query = {}
        
        if id: query["Id"] = id
        if total: query["total"] = total
        if downloaded: query["downloaded"] = downloaded
        if avg_rating: query["avg rating"] = avg_rating
        if reviews: query["reviews"] = reviews
        result = collection.find(query)

        for document in result:
            var = (document["Id"], document["total"], document["downloaded"], document["avg rating"], document["reviews"])
            print(var)
        
        return query, result

    def sort_data(self, collection_name, query, sort):
        collection = self.db[collection_name]
        result = collection.find(query).sort(sort)

        for document in result:
            print(document)
        return result

    def reset_data(self):
        # open json files
        with open('Data/out.json', 'r') as json_file:
            item_data = json.load(json_file)

        with open('Data/out_review.json', 'r') as json_review_file:
            review_data = json.load(json_review_file)
        
        # go through items in file
        i = 0
        i_max = 10

        # get data and reset it
        data_collection = self.db[DATA_COLLECTION_NAME]
        data_collection.drop()
        data_collection.insert_many(item_data[:i_max])

        # get review data and reset it
        review_collection = self.db[REVIEW_COLLECTION_NAME]
        review_collection.drop()
        review_collection.insert_many(review_data[:i_max])
    
    def get_client(self):
        return self.client