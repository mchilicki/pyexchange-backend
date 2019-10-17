from django.core.management.base import BaseCommand, CommandError
from pyexchange.models import Currency
import coreapi


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = coreapi.Client()
        nbp_currencies = client.get('http://api.nbp.pl/api/exchangerates/tables/C/')
        for nbp_rate in nbp_currencies[0]['rates']:
            currency, created = Currency.objects.get_or_create(
                code=nbp_rate['code'],
                defaults={
                    "name": nbp_rate['currency'],
                    "code": nbp_rate['code'],
                    "unit": 1,
                    "purchase_price": nbp_rate['ask'],
                    "sell_price": nbp_rate['bid'],
                }
            )
            if not created:
                currency.purchase_price = nbp_rate['ask']
                currency.sell_price = nbp_rate['bid']
            currency.save()
