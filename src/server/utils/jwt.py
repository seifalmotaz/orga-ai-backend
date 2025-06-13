import os
import jwt
from dataclasses import dataclass
import time

@dataclass
class TokenPayload:
    user_id: str
    exp: int


def decode_access_token(token: str):
    payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    return TokenPayload(**payload)


def create_access_token(user_id: str):
    payload = TokenPayload(user_id=user_id, exp=time.time() + 3600)
    return jwt.encode(payload.model_dump(), os.getenv("JWT_SECRET"), algorithm="HS256")