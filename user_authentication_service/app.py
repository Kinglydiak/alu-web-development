#!/usr/bin/env python3
"""Flask app module exposing the routes of the authentication service."""
from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Return a JSON payload containing a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Register a new user from the form data and return a JSON payload,
    or a 400 error if the email is already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Log a user in from the form data, set the session_id cookie and
    return a JSON payload, or respond with a 401 error on bad credentials.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Log the user out by destroying the session found in the session_id
    cookie and redirecting to the root, or respond with a 403 error if no
    user matches the session.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """Return a JSON payload with the email of the user matching the
    session_id cookie, or respond with a 403 error if no user matches.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
