from rest_framework import generics
from .models import DivergenceScreener
from .serializers import DivergenceScreenerSerializer,BrakerScreenerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class DivergenceScreenerCreateView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'datadict': openapi.Schema(type=openapi.TYPE_OBJECT),
                'interval': openapi.Schema(type=openapi.TYPE_STRING),
                'currentprice': openapi.Schema(type=openapi.TYPE_STRING),
                'symbol': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['datadict', 'interval', 'currentprice', 'symbol'],
        ),
        responses={
            201: 'Created',
            400: 'Bad Request',
        },
        operation_summary="Create a Divergence Screener",
    )
    def post(self, request, *args, **kwargs):
        serializer = DivergenceScreenerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BrakerScreenerCreateView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notification': openapi.Schema(type=openapi.TYPE_STRING),
                'interval': openapi.Schema(type=openapi.TYPE_STRING),
                'currentprice': openapi.Schema(type=openapi.TYPE_STRING),
                'symbol': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['notification', 'interval', 'currentprice', 'symbol'],
        ),
        responses={
            201: 'Created',
            400: 'Bad Request',
        },
        operation_summary="Create a Divergence Screener",
    )
    def post(self, request, *args, **kwargs):
        serializer = BrakerScreenerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)