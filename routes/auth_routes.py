import base64
import hashlib
import hmac

import boto3
from flask import Blueprint, request, jsonify

from config import Config

auth_bp = Blueprint("auth", __name__)

cognito_client = boto3.client("cognito-idp", region_name=Config().COGNITO_REGION_NAME)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Calculate SECRET_HASH if necessary
        secret_hash = calculate_secret_hash(Config().COGNITO_CLIENT_ID, Config().COGNITO_CLIENT_SECRET, username)

        # Call Cognito's InitiateAuth
        response = cognito_client.initiate_auth(
            ClientId=Config().COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,  # Include only if the app client has a secret
            },
        )

        # Check if AuthenticationResult is in the response
        if "AuthenticationResult" in response:
            return jsonify({"token": response["AuthenticationResult"]}), 200
        else:
            return jsonify({"error": "Authentication failed. Check your credentials."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def calculate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    dig = hmac.new(
        client_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()
