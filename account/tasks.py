from celery import shared_task

from decimal import Decimal
import requests
from celery import shared_task
from currency.models import Rate
from currency import model_choices as mch


def save(source, rate_kwargs):
    new_rate = Rate(**rate_kwargs)
    last_rate = Rate.objects.filter(
        currency=rate_kwargs['currency'],
        source=source,
        ).last()
    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def privat():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    for rate in response.json():
        if rate['ccy'] in {'USD', 'EUR'}:
            currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_PRIVAT,
            }
            save(mch.SR_PRIVAT, rate_kwargs)


def vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    for key, rate in response.json().items():
        if key in {'Dollar', 'Euro'}:
            if key == 'Dollar':
                currency = mch.CURR_USD
            else:
                currency = mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_VKURSE,
            }
            save(mch.SR_VKURSE, rate_kwargs)


def mono():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    for rate in response.json():
        if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] == 980:
            mono_code = {
                840: mch.CURR_USD,
                978: mch.CURR_EUR,
            }

            currency = mono_code[rate['currencyCodeA']]

            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(str(round(rate['rateBuy'], 2))),
                'sale': Decimal(str(round(rate['rateSell'], 2))),
                'source': mch.SR_MONO,
            }
            save(mch.SR_MONO, rate_kwargs)


def nbu():
    url = 'https://old.bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    for key, rate in response.json().items():
        if key in {'Dollar', 'Euro'}:
            if key == 'Dollar':
                currency = mch.CURR_USD
            else:
                currency = mch.CURR_EUR
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_NBU,
            }
            save(mch.SR_NBU, rate_kwargs)


@shared_task()
def parse_rates():
  privat()
  mono()
  vkurse()
  nbu()


@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

