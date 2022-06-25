from locale import currency
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Anime, anime_schema, animes_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/animes', methods = ['POST'])
@token_required
def create_anime(current_user_token):
    name = request.json['name']
    character = request.json['character']
    quote = request.json['quote']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    anime = Anime(name, character, quote, user_token = user_token )

    db.session.add(anime)
    db.session.commit()

    response = anime_schema.dump(anime)
    return jsonify(response)

@api.route('/animes', methods = ['GET'])
@token_required
def get_anime(current_user_token):
    a_user = current_user_token.token
    animes = Anime.query.filter_by(user_token = a_user).all()
    response = animes_schema.dump(animes)
    return jsonify(response)



#Update End point
@api.route('animes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_anime(current_user_token, id):
    anime = Anime.query.get(id)
    anime.name = request.json['name']
    anime.character = request.json['character']
    anime.quote = request.json['quote']
    anime.user_token = current_user_token.token

    db.session.commit()
    response = anime_schema.dump(anime)
    return jsonify(response)

# Delete Endpoint
@api.route('/animes/<id>', methods = ['DELETE'])
@token_required
def delete_anime(current_user_token, id):
    anime = Anime.query.get(id)
    db.session.delete(anime)
    db.session.commit()
    response = anime_schema.dump(anime)
    return jsonify(response)

# detailed routes for my animes