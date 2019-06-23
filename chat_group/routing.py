from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import home.routing

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(home.routing.websocket_urlpatterns))}
)

