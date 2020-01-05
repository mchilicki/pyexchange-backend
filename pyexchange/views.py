from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from pyexchange.serializers import CurrencySerializer, UserCurrencySerializer, UserSerializer
from pyexchange.models import Currency, UserCurrency, Profile
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction

from pyexchange.utils.users import is_username_free, is_email_free, check_password


class CurrencyViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [AllowAny]
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
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
        return Response(UserSerializer(instance=user).data)


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    detail_serializer_class = UserSerializer
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get(self, request):
        return Response(UserSerializer(instance=request.user).data)
