import os
import pymongo
from flask import Flask, jsonify, request
from bson import json_util

client = pymongo.MongoClient(os.getenv('MONGO_URL', 'localhost'))
db = client['movies-data']["movies"]

app = Flask(__name__)


@app.route('/', methods=["GET"])
def health():
    return 'ok'


@app.route('/movies', methods=["GET"])
def get_movies():
    movies = list(db.find(request.args.to_dict(), {"_id": False}))
    return jsonify({"movies": movies, "count": len(movies)})


@app.route('/movies/<movie_id>', methods=["GET"])
def get_movie(movie_id):
    q = db.find_one({"id": movie_id}, {"_id": False})
    if q:
        return q, 200
    return jsonify(success=False, error="Not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)