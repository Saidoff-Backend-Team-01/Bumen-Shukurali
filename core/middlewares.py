from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
import jwt
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token):

    token = jwt.decode(token)
    return token.user



class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        print(headers)
        if b'Authorization' in headers:
            token_name, token_key = headers[b'Authorization'].decode().split()
            print("token", token_name, token_key)

            if token_name == 'Token':
                scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)
