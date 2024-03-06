from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "App"
    def ready(self):
        from .scheduler import scheduler,start_socket_job
        from App.models import DivergenceScreener ,BrakerScreener
        from App.singlas import divergence_screener_post_save , braker_screener_post_save
        from django.db.models.signals import post_save
        post_save.connect(divergence_screener_post_save, sender=DivergenceScreener)
        post_save.connect(braker_screener_post_save, sender=BrakerScreener)
        scheduler.start()
        start_socket_job()
