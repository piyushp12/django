from django.urls import path
from App.consumers import BrakerScreenerConsumer,DivergenceScreenerConsumer, BrakerScreenerConsumerNew

websocket_router = [
    # path("braker_screener/", BrakerScreenerConsumer.as_asgi()),
    # path("divergence_screener/", DivergenceScreenerConsumer.as_asgi()),
    path("arpit-lodu/", BrakerScreenerConsumerNew.as_asgi()),
]