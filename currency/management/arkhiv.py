from datetime import datetime, timedelta, date
import requests
from django.core.management.base import BaseCommand
from decimal import Decimal
from currency import model_choices as mch
from currency.models import Rate

class Command(BaseCommand):
    help = 'Archive rates from PrivataBank for last 4 years ago'

    def handle(self, *args, **options):

        for day in range(365 * 4):
            date = datetime.now() + timedelta(days=-day)
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.day}.{date.month}.{date.year}'
            response = requests.get(url)
            r_json = response.json()

            for rate in r_json()["exchangeRate"]:
                if rate.get('currency') is not None:
                    if rate['currency'] in {'USD', 'EUR'}:
                        currency = mch.CURR_USD if rate['currency'] == 'USD' else mch.CURR_EUR
                        rate_kwargs = {
                            'currency': currency,
                            'buy': Decimal(rate['purchaseRate']),
                            'sale': Decimal(rate['saleRate']),
                            'source': mch.SR_PRIVAT,
                        }
                        new_rate = Rate(**rate_kwargs)
                        last_rate = Rate.objects.filter(currency=currency, source=mch.SR_PRIVAT).last()

                        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                            new_rate.save()
