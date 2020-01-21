from django.contrib.auth.models import User
from rest_framework import serializers
from pyexchange.models import Currency, UserCurrency, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'money'
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'code', 'unit', 'purchase_price'
        )


class BoughtCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'code', 'unit', 'sell_price', 'purchase_price'
        )


class UserCurrencySerializer(serializers.ModelSerializer):
    currency = BoughtCurrencySerializer(read_only=True)

    class Meta:
        model = UserCurrency
        fields = (
            'id', 'amount', 'currency'
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    currencies = UserCurrencySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'profile', 'currencies'
        )
