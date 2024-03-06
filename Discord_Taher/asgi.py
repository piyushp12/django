# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Discord_Taher.settings")

# application = get_asgi_application()


import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import App.rountings as route

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Discord_Taher.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(route.websocket_router)
})