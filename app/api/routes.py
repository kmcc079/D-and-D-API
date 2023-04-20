from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Character, char_schema, charas_schema

api = Blueprint('api', __name__, url_prefix='/api')

# create new character
@api.route('/characters', methods = ['POST'])
@token_required
def new_character(current_user_token):
    name = request.json['name']
    race = request.json['race']
    _class = request.json['_class']
    alignment = request.json['alignment']
    background = request.json['background']
    level = request.json['level']
    experience = request.json['experience']
    user_token = current_user_token.token

    character = Character(name, race, _class, alignment, background, level, experience, user_token=user_token)

    db.session.add(character)
    db.session.commit()

    response = char_schema.dump(character)
    return jsonify(response)


# get all characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    a_user = current_user_token.token
    characters = Character.query.filter_by(user_token=a_user).all()

    response = charas_schema.dump(characters)
    return jsonify(response)


# get info for one character
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_single_character(current_user_token, id):
    character = Character.query.get(id)

    response = char_schema.dump(character)
    return jsonify(response)


# update character info
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)
    character.name = request.json['name']
    character.race = request.json['race']
    character._class = request.json['_class']
    character.alignment = request.json['alignment']
    character.background = request.json['background']
    character.level = request.json['level']
    character.experience = request.json['experience']
    character.user_token = current_user_token.token

    db.session.commit()

    response = char_schema.dump(character)
    return jsonify(response)


# delete a character
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    
    db.session.delete(character)
    db.session.commit()

    response = char_schema.dump(character)
    return jsonify(response)