from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from pyexchange.serializers import CurrencySerializer, UserCurrencySerializer
from pyexchange.models import Currency, UserCurrency, Profile
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction


class CurrencyViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [AllowAny]
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer


class UserCurrencyViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserCurrency.objects.all().order_by('name')
    serializer_class = UserCurrencySerializer

    @action(detail=False, methods=['get'])
    def get_mine(self, request):
        user = request.user
        filtered_currencies = UserCurrency.objects.filter(owner_id=user.id)
        serialized_data = UserCurrencySerializer(filtered_currencies, many=True).data
        return Response(serialized_data)

    @action(detail=True, methods=['post'])
    def buy(self, request, pk):
        user = request.user
        profile = Profile.objects.get(user=user)
        currency = Currency.objects.get(pk=pk)
        amount = request.data['amount']
        user_money_costs = amount * currency.sell_price / currency.unit
        if user_money_costs > profile.money:
            return Response({'error': "User doesn't have enough founds"}, status=status.HTTP_400_BAD_REQUEST)
        if amount % currency.unit != 0:
            return Response({'error': "Amount is not multiple of unit"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            user_currency, created = UserCurrency.objects.get_or_create(currency=currency, owner=user)
            user_currency.amount += amount
            profile.money -= user_money_costs
            profile.save()
            user_currency.save()
        return Response({'currency-amount': user_currency.amount}, status=status.HTTP_200_OK)
