from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from pyexchange.serializers import CurrencySerializer
from pyexchange.models import Currency
from rest_framework.permissions import IsAuthenticated, AllowAny


class CurrencyViewSet(GenericViewSet, ListModelMixin):
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer
