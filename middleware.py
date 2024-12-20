from functools import wraps

import jwt
import requests
from flask import request, jsonify
from jwt import InvalidTokenError, ExpiredSignatureError

from config import Config


def cognito_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401

        try:
            # Extract the token
            token = token.split(" ")[1] if " " in token else token

            # Fetch JWKS from Cognito
            jwks = get_cognito_keys()

            # Decode the token (replace 'your-jwks-url' with Cognito JWKs URL)
            decoded_access_token = validate_token(token, jwks)

            # Extract user info
            cognito_sub = decoded_access_token["sub"]
            username = decoded_access_token["username"]
            groups = decoded_access_token.get("cognito:groups", [])

            request.user = cognito_sub
            request.user_groups = groups
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    wrapper.__name__ = func.__name__
    return wrapper


def get_cognito_keys():
    """Fetch Cognito JSON Web Key Sets (JWKS)"""
    url = f"https://cognito-idp.{Config().COGNITO_REGION_NAME}.amazonaws.com/{Config().COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def validate_token(token, jwks, audience=None):
    """Validate a JWT token using JWKS"""
    try:
        # Decode token header to get the key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Find the correct key in JWKS
        key = next((key for key in jwks['keys'] if key["kid"] == kid), None)
        if not key:
            raise InvalidTokenError("Key not found in JWKS")

        # Construct public key
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        # Decode and validate the token
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=audience,
            options={"verify_exp": True}
        )
        return decoded_token

    except ExpiredSignatureError:
        raise Exception(f"Token validation failed: Token has expired")
    except InvalidTokenError as e:
        raise Exception(f"Token validation failed: Invalid token: {e}")
    except Exception as e:
        print(f"Token validation failed: {e}")
    return None


# Admin role check decorator
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_groups = getattr(request, "user_groups", [])
        if "admin" not in user_groups:
            return jsonify({"error": "Admin privileges required"}), 403
        return func(*args, **kwargs)

    return wrapper
