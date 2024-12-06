from django.urls import re_path , include
from supject.consumers import GeneralChatConsumer, SujectChatConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path("ws/general/" , GeneralChatConsumer.as_asgi()) , 
    re_path(r"ws/clubchat/(?P<room_name>\w+)/$", SujectChatConsumer.as_asgi()),
] 

