from robyn import Request
from robyn.authentication import AuthenticationHandler, Identity
from src.database.models import User
from src.server.utils.jwt import decode_access_token


class BasicAuthHandler(AuthenticationHandler):
    async def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)

        try:
            payload = decode_access_token(token)
            clerk_id = payload["sub"]
        except Exception as e:
            print(e)
            return None

        user = await User.get(clerk_id=clerk_id)

        return Identity(claims={"user": f"{user}"})
