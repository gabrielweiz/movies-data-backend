import os

import pymongo
import uuid


class MoviesPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGO_URL', 'localhost'))
        self.db = self.client['movies-data']["movies"]

    def process_item(self, item, spider):
        existing_obj = self.db.find_one({"title": item['title']})
        updates = {}
        if existing_obj:
            if item.get("rotten_tomatoes_critics_rating"):
                updates["rotten_tomatoes_critics_rating"] = item["rotten_tomatoes_critics_rating"]
            if item.get("rotten_tomatoes_audience_rating"):
                updates["rotten_tomatoes_audience_rating"] = item["rotten_tomatoes_audience_rating"]
            if item.get("imdb_rating"):
                updates["imdb_rating"] = item["imdb_rating"]

            updates["stars"] = list(set(existing_obj['stars'] + item['stars']))

            self.db.find_one_and_update({"title": item['title']},
                                        {"$set": updates})

            print(f"updated movie {item['title']}")
        else:
            dict_item = dict(item)
            dict_item["id"] = uuid.uuid4().hex
            dict_item["stars"] = list(set(item['stars']))
            self.db.insert_one(dict_item)
            print(f"inserted movie {item['title']}")
        return item