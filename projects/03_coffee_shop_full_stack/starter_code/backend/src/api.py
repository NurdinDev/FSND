import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"*": {"origins": "*"}})

db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    """Public: Get Drinks list as short object"""

    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    """Get Drinks list"""
    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    """Add New Drink"""
    body = request.get_json()
    if not body or 'title' not in body:
        abort(400)

    try:
        drink = Drink(title=body.get('title', None),
                      recipe=str(body.get('recipe', None)).replace("\'", "\""))
        drink.insert()

        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in Drink.query.all()]
        })
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    drinkJson = request.get_json()
    title = drinkJson.get("title", None)
    recipe = drinkJson.get('recipe', None)

    if title:
        drink.title = title
    if recipe:
        drink.recipe = str(recipe).replace("\'", "\"")

    drink.update()

    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    })


@app.route('/drinks/<int:drinkId>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drinkId):
    drink = Drink.query.get(drinkId)
    if not drink:
        abort(404)

    drink.delete()

    return jsonify({
        'success': True,
        'delete': drinkId
    })


# Error Handling
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found!"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': "internal server error!"
    }), 500


@app.errorhandler(400)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad Request!"
    }), 400


@app.errorhandler(AuthError)
def handle_invalid_usage(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
