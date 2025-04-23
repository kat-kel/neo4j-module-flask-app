from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import current_user, jwt_required

from api.dao.genres import GenreDAO
from api.dao.movies import MovieDAO

genre_routes = Blueprint("genre", __name__, url_prefix="/api/genres")


@genre_routes.get("/")
def get_index():
    # Create the DAO
    dao = GenreDAO(current_app.driver)

    # Get output
    output = dao.all()

    return jsonify(output)


@genre_routes.get("/<name>/")
def get_genre(name):
    # Create the DAO
    dao = GenreDAO(current_app.driver)

    # Get the Genre
    output = dao.find(name)

    return jsonify(output)


@genre_routes.get("/<name>/movies")
@jwt_required(optional=True)
def get_genre_movies(name):

    # Extract pagination values from the request
    sort = request.args.get("sort", "title")
    order = request.args.get("order", "ASC")
    limit = request.args.get("limit", 6, type=int)
    skip = request.args.get("skip", 0, type=int)

    # Get User ID from JWT Auth
    user_id = current_user["sub"] if current_user != None else None

    # Create a new MovieDAO Instance
    dao = MovieDAO(current_app.driver)

    # Retrieve a paginated list of movies
    output = dao.get_by_genre(name, sort, order, limit, skip, user_id)

    return jsonify(output)
