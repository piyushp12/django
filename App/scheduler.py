from apscheduler.schedulers.background import BackgroundScheduler
# from your_app.models import MyUser
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from App.serializers import *
channel_layer = get_channel_layer()
import json
from .models import *
misfire_grace_time = 600
max_instances = 200

scheduler=BackgroundScheduler()

def send_data_to_socket():
    data = BrakerScreener.objects.all()
    serializer = BrakerScreenerSerializerData(data, many=True)
    divergencs=DivergenceScreener.objects.all()
    divergence_data=DivergenceScreenerSerializerData(divergencs, many=True)
    async_to_sync(channel_layer.group_send)(
        "braker_data",  
        {
            "type": "send_braker_notification",
            "instance": serializer.data,
        },
    )
    async_to_sync(channel_layer.group_send)(
        "braker_data",  
        {
            "type": "send_divergence_notification",
            "instance": divergence_data.data,
        },
    )
def start_socket_job():
    return scheduler.add_job(send_data_to_socket, trigger='interval', seconds=5, misfire_grace_time=misfire_grace_time, max_instances=max_instances)



