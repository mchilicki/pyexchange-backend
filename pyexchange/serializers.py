from rest_framework import serializers
from pyexchange.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'code', 'unit', 'purchase_price', 'sell_price',
        )



