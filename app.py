import os
import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

client = pymongo.MongoClient(os.getenv('MONGO_URL', 'localhost'))
db = client['movies-data']["movies"]

app = Flask(__name__)
CORS(app)



@app.route('/', methods=["GET"])
def health():
    return 'ok'


"""
Rota que aceita qualquer filtro simples passado.
Pro caso de "stars" e "director" ele aceita um filtro composto usando "OR" entre os valores,
Dessa forma retornando filmes que possuem um OU outro valor.
Para o campo stars também é possível usar "AND", dessa forma retornando filmes que possuem os dois valores
Também é possivel filtrar os filmes com valor maior ou menor igual com os campos de número utilizando => ou <=

Exemplos:

http://192.168.15.74:7000/movies?director=Frank%20CapraORSteven%20Spielberg
retorna os filmes de ambos diretores

http://192.168.15.74:7000/movies?year>=2005
retorna os filmes a partir de 2005

http://192.168.15.74:7000/movies?rotten_tomatoes_critics_rating>=99
filmes com score 99 ou mais pelos criticos do rotten tomatoes

http://192.168.15.74:7000/movies?rotten_tomatoes_critics_rating>=99&rotten_tomatoes_audience_rating>=95&imdb_rating>=8.4
filmes com score >= 99 rotten_tomatoes_critics_rating >= 95 rotten_tomatoes_audience_rating e >= 8.4 score no imdb

http://192.168.1.12:7000/movies?stars=Dean%20GordonANDNatalie%20Morales
retorna os filmes em que os 2 atores atuam juntos

"""
@app.route('/movies', methods=["GET"])
def get_movies():
    query = {}
    for k, v in request.args.to_dict().items():
        if (k == "stars" or k == "director") and "OR" in v:
            query[k] = {"$in": v.split("OR")}
        elif (k == "stars" or k == "director") and "AND" in v:
            query['$and'] = [{k: val} for val in v.split("AND")]
        elif ">" in k or "<" in k:
            query[k[:-1]] = {"$gte" if ">" in k else "$lte": float(v) if "imdb_rating" in k else int(v)}
        elif "rating" in k or k == "year":
            query[k] = float(v) if k == "imdb_rating" else int(v)
        else:
            query[k] = v

    movies = list(db.find(query, {"_id": False}))
    return jsonify({"movies": movies, "count": len(movies)})


@app.route('/movies/<movie_id>', methods=["GET"])
def get_movie(movie_id):
    q = db.find_one({"id": movie_id}, {"_id": False})
    if q:
        return q, 200
    return jsonify(success=False, error="Not found"), 404


@app.route('/directors', methods=["GET"])
def list_directors():
    response = {}
    for d in list(db.find({}, {"director": True}).distinct("director")):
        response[d] = db.count({"director": d})
    return jsonify(response)


@app.route('/stars', methods=["GET"])
def list_stars():
    response = {}
    for s in list(db.find({}, {"stars": True}).distinct("stars")):
        response[s] = db.count({"stars": s})
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)