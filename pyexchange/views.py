from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from pyexchange.serializers import CurrencySerializer
from pyexchange.models import Currency


class CurrencyViewSet(GenericViewSet, ListModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
