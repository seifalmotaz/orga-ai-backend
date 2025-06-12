import jwt

import os


def decode_access_token(token: str):
    return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
