from rest_framework import serializers
from .models import *
from django.contrib.contenttypes.models import ContentType
class DivergenceScreenerSerializer(serializers.Serializer):
    datadict=serializers.JSONField(write_only=True)
    interval=serializers.CharField(write_only=True)
    currentprice=serializers.CharField(write_only=True)
    symbol=serializers.CharField(write_only=True)
    time=serializers.CharField(write_only=True)
    interval_mapping = {
        "15 minutes interval": "15m",
        "1 hour interval": "1h",
        "4 hours interval": "4h",
        "1 day interval": "1d",
        "1 week interval": "1w",
    }
    def map_alert_to_divergence(self,alert):
        """
        Maps an alert to its corresponding divergence code based on a predefined mapping.

        Parameters:
            alert (str): The alert message to be mapped to a divergence code.

        Returns:
            str or None: The divergence code corresponding to the alert, or None if no matching divergence is found.
        """
        divergence_mapping = {
            'Bearish Regular Divergence': 'BERD',
            'Bearish Hidden Divergence': 'BEHD',
            'Bullish Regular Divergence': 'BURD',
            'Bullish Hidden Divergence': 'BUHD',
        }

        for divergence, code in divergence_mapping.items():
            if divergence in alert:
                return code

        return None
    def find_model_instance_by_symbol(self,symbol):
        """
        Find a model instance by symbol.

        :param symbol: The symbol to search for.
        :type symbol: str
        :return: The model instance with the given symbol, or None if not found.
        :rtype: Union[CryptoTotalMarket, None]
        """
        models = [
            CryptoTotalMarket,
        ]

        for model in models:
            try:
                instance = model.objects.get(exchange=symbol)
                return instance
            except model.DoesNotExist:
                continue

        return None
    def create(self, validated_data):
        """

        Args:
            validated_data: The validated data to create the instance from.

        Returns:
            The created DivergenceScreener instance, or None if no instance is created.
        """
        instance = self.find_model_instance_by_symbol(validated_data['symbol'])
        if instance:
            for item in validated_data['datadict'].values():
                rsi=item.get('rsi_alerts', [])
                obv=item.get('obv_alerts', [])
                stochastics=item.get('stochastics_alerts', [])
                cvd=item.get('cvd_alerts', [])
                macd_histogram=item.get('macd_alerts', [])
                divergence_screener_instance = DivergenceScreener.objects.create(
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.id,
                    interval=self.interval_mapping.get(validated_data['interval']),
                    price=float(validated_data['currentprice']),
                    rsi=self.map_alert_to_divergence(rsi[0]) if rsi else None,
                    obv=self.map_alert_to_divergence(obv[0]) if obv else None,
                    stochastics=self.map_alert_to_divergence(stochastics[0]) if stochastics else None,
                    cvd=self.map_alert_to_divergence(cvd[0]) if cvd else None,
                    macd_histogram=self.map_alert_to_divergence(macd_histogram[0]) if macd_histogram else None,
                    time=validated_data['time'],
                )
                return divergence_screener_instance
        return None
            
            
class BrakerScreenerSerializer(serializers.Serializer):
    notification=serializers.CharField(write_only=True)
    interval=serializers.CharField(write_only=True)
    currentprice=serializers.CharField(write_only=True)
    symbol=serializers.CharField(write_only=True)
    is_support=serializers.BooleanField(write_only=True)
    level=serializers.CharField(write_only=True)
    time=serializers.CharField(write_only=True)
    interval_mapping = {
        "15 minutes": "15m",
        "1 hour": "1h",
        "4 hours": "4h",
        "1 day": "1d",
        "1 week": "1w",
    }
    def find_model_instance_by_symbol(self,symbol):
        models = [
            CryptoTotalMarket,
        ]

        for model in models:
            try:
                instance = model.objects.get(exchange=symbol)
                return instance
            except model.DoesNotExist:
                continue

        return None
    def create(self, validated_data):
        instance = self.find_model_instance_by_symbol(validated_data['symbol'])
        if instance:
            brakere_screener_instance = BrakerScreener.objects.create(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.id,
                interval=self.interval_mapping.get(validated_data['interval']),
                price=float(validated_data['currentprice']),
                notification=validated_data['notification'],
                is_support=validated_data['is_support'],
                level=validated_data['level'],
                time=validated_data['time'],
                
            )
            return brakere_screener_instance
        return None
    


class CryptoPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPair
        fields = ['pair','exchange']

class CommoditiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodities
        fields = ['pair','exchange']

class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forex
        fields = ['pair','exchange']

class IndStockMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndStockMarket
        fields = ['pair','exchange']

class UsStockMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsStockMarket
        fields = ['pair','exchange']

class WorldMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldMarket
        fields = ['pair','exchange']

class CryptoTotalMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTotalMarket
        fields = ['pair','exchange']
        

class DivergenceScreenerSerializerData(serializers.ModelSerializer):
    exchange = serializers.SerializerMethodField()

    class Meta:
        model = DivergenceScreener
        fields = ['content_type','object_id','exchange','price','rsi','macd_histogram','obv','cvd','stochastics','interval', 'time']

    def get_exchange(self, obj):
        if obj.content_type.model == 'cryptopair':
            serializer = CryptoPairSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'commodities':
            serializer = CommoditiesSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'forex':
            serializer = ForexSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'indstockmarket':
            serializer = IndStockMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'usstockmarket':
            serializer = UsStockMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'worldmarket':
            serializer = WorldMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'cryptototalmarket':
            serializer = CryptoTotalMarketSerializer(obj.exchange, context=self.context)
        else:
            return None

        return serializer.data



class BrakerScreenerSerializerData(serializers.ModelSerializer):
    exchange = serializers.SerializerMethodField()

    class Meta:
        model = BrakerScreener
        fields = ['content_type','object_id','exchange','price','notification','interval','created_at','is_support','level', 'time']

    def get_exchange(self, obj):
        if obj.content_type.model == 'cryptopair':
            serializer = CryptoPairSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'commodities':
            serializer = CommoditiesSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'forex':
            serializer = ForexSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'indstockmarket':
            serializer = IndStockMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'usstockmarket':
            serializer = UsStockMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'worldmarket':
            serializer = WorldMarketSerializer(obj.exchange, context=self.context)
        elif obj.content_type.model == 'cryptototalmarket':
            serializer = CryptoTotalMarketSerializer(obj.exchange, context=self.context)
        else:
            return None

        return serializer.data
    
    
class LoduScreenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrakerScreener
        fields = '__all__'