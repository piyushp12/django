from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import *
from .api_views import *
urlpatterns = [
  path('', BreakerScreenerListView.as_view(), name='breaker_screener_list'),
  path('divergence_screener/', DivergenceScreenerListView.as_view(), name='divergence_screener_list'),
  path('api/divergencescreener/create/', DivergenceScreenerCreateView.as_view(), name='divergence'),
  path('api/brakergencescreener/create/', BrakerScreenerCreateView.as_view(), name='breacker'),
]