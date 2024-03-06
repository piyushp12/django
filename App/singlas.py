from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DivergenceScreener, BrakerScreener
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from App.serializers import *
channel_layer = get_channel_layer()

@receiver(post_save, sender=DivergenceScreener)
def divergence_screener_post_save(sender, instance, created, **kwargs):
    if created:
        serializer = DivergenceScreenerSerializerData(instance)
        async_to_sync(channel_layer.group_send)(
            "divergence",  # Use the group for DivergenceScreener events
            {
                "type": "send_divergence_notification",
                "instance": json.dumps(serializer.data),
            },
        )
        print(f'DivergenceScreener {instance} created!')

@receiver(post_save, sender=BrakerScreener)
def braker_screener_post_save(sender, instance, created, **kwargs):
    if created:
        serializer = BrakerScreenerSerializerData(instance)
        async_to_sync(channel_layer.group_send)(
            "braker",  # Use the group for BrakerScreener events
            {
                "type": "send_braker_notification",
                "instance": json.dumps(serializer.data),
            },
        )
        print(f'BrakerScreener {instance} created!')
