from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')


class LoginView(View):
    template_name = 'login.html' 

    def get(self, request):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard_view'))
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard_view'))
        else:
            emailRaw = request.POST.get('email')
            email = emailRaw.lower()
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard_view'))
                else:
                    messages.error(request, 'Your account is not active.')
            else:
                messages.error(request, 'Invalid login credentials.')

            return render(request, self.template_name)


class DashboardView(View):
  
    def get(self, request):
        print("request.user.is_authenticated---",request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'dashboard.html')

    def post(self, request):
        model = request.POST.get('model')
        return redirect('list_view', model=model)




class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')


class ListView(View):

    def get(self, request, model):
        print("request.user.is_authenticated---",request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect('login')


        search_query = request.GET.get('search')
        data=None
        if model == 'crypto':
            data = CryptoPair.objects.all()
        elif model == 'commodities':
            data = Commodities.objects.all()
        elif model == 'forex':
            data = Forex.objects.all()
        elif model == 'ind_stock_market':
            data = IndStockMarket.objects.all()
        elif model == 'us_stock_market':
            data = UsStockMarket.objects.all()
        elif model == 'world_market':
            data = WorldMarket.objects.all()
        elif model == 'crypto_total_market':
            data = CryptoTotalMarket.objects.all()

        if search_query:
            data = data.filter(exchange__icontains=search_query)

        paginator = Paginator(data, 10)  # Change 10 to the number of items per page you want

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'listView.html', {'model': model, 'data': page_obj, 'search_query': search_query})

    def post(self, request, model):
            exchange = request.POST.get('exchange')
            symbol = request.POST.get('symbol')

            print(exchange, symbol)

            if model == 'crypto' and exchange and symbol:
                # Check if the CryptoPair already exists
                if CryptoPair.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    CryptoPair.objects.create(exchange=exchange, pair=symbol)
            elif model == 'commodities' and exchange and symbol:
                # Check if the Commodities already exists
                if Commodities.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    Commodities.objects.create(exchange=exchange, pair=symbol)
            elif model == 'forex' and exchange and symbol:
                # Check if the Forex already exists
                if Forex.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    Forex.objects.create(exchange=exchange, pair=symbol)
            elif model == 'ind_stock_market' and exchange and symbol:
                # Check if the IndStockMarket already exists
                if IndStockMarket.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    IndStockMarket.objects.create(exchange=exchange, pair=symbol)
            elif model == 'us_stock_market' and exchange and symbol:
                # Check if the UsStockMarket already exists
                if UsStockMarket.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    UsStockMarket.objects.create(exchange=exchange, pair=symbol)
            elif model == 'world_market' and exchange and symbol:
                # Check if the WorldMarket already exists
                if WorldMarket.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    WorldMarket.objects.create(exchange=exchange, pair=symbol)
            elif model == 'crypto_total_market' and exchange and symbol:
                # Check if the CryptoTotalMarket already exists
                if CryptoTotalMarket.objects.filter(exchange=exchange, pair=symbol).exists():
                    messages.error(request, f"The pair value '{symbol}' for the exchange '{exchange}' already exists.")
                else:
                    CryptoTotalMarket.objects.create(exchange=exchange, pair=symbol)

            return redirect('list_view', model=model)
        


class TestView(View):
    def get(self, request): 
        return render(request, 'test.html')


def delete_crypto_pair(request, pk):
    crypto_pair = get_object_or_404(CryptoPair, pk=pk)
    crypto_pair.delete()
    return redirect('list_view', model='crypto')

def delete_forex(request, pk):
    forex = get_object_or_404(Forex, pk=pk)
    forex.delete()
    return redirect('list_view', model='forex')

def delete_commodities(request, pk):
    forex = get_object_or_404(Commodities, pk=pk)
    forex.delete()
    return redirect('list_view', model='commodities')

def delete_ind_stock_market(request, pk):
    forex = get_object_or_404(IndStockMarket, pk=pk)
    forex.delete()
    return redirect('list_view', model='ind_stock_market')


def delete_us_stock_market(request, pk):
    forex = get_object_or_404(UsStockMarket, pk=pk)
    forex.delete()
    return redirect('list_view', model='us_stock_market')

def delete_crypto_total_market(request, pk):
    forex = get_object_or_404(CryptoTotalMarket, pk=pk)
    forex.delete()
    return redirect('list_view', model='crypto_total_market')


def delete_world_market(request, pk):
    forex = get_object_or_404(WorldMarket, pk=pk)
    forex.delete()
    return redirect('list_view', model='world_market')


from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from App.serializers import *
channel_layer = get_channel_layer()

class BreakerScreenerListView(View):
    template_name = 'breaker_screener_list.html'
    def get(self, request):
        all_pair = CryptoTotalMarket.objects.all()
        return render(request, self.template_name,{"all_pair":all_pair})
    


class DivergenceScreenerListView(View):
    template_name = 'divergence_screener_list.html'

    def get(self, request):
        all_pair = CryptoTotalMarket.objects.all()
        return render(request, self.template_name,{"all_pair":all_pair})