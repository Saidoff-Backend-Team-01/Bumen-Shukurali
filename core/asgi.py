import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from channels.routing import URLRouter



from supject.routings import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket" : JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
