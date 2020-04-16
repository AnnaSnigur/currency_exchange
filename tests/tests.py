import pytest
from django.urls import reverse
from decimal import Decimal
from account.models import User, Contact
from currency.models import Rate
from currency.tasks import _privat, _mono
from django.core import mail
from account.tasks import send_activation_code_async
from uuid import uuid4


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


def test_rates_not_auth(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user.username, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_rates(api_client, user):
    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


class Response:
    pass


def test_task(mocker):
    def mock():
        response = Response()
        response.json = lambda: [{'ccy': 'USD'}]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _privat()


def test_send_email():
    emails = mail.outbox
    print('EMAILS:', emails)

    send_activation_code_async.delay(1, str(uuid4()))
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'


def test_smoke(client):
    response = client.get(reverse('account:smoke'))
    assert response.status_code == 200


def test_get_contact(api_client, user):
    url = reverse('api-currency:contacts')
    response = api_client.get(url)
    assert response.status_code == 200


def test_post_contact(api_client, user):
    url = reverse('api-currency:contacts')
    response = api_client.post(
        url,
        data={
            'email': 'python.it.ua@mail.com',
            'title': 'title',
            'text': 'text'
        },
        format='json'
    )
    assert response.status_code == 201


def test_dell_contact(api_client, user):
    url = reverse('api-currency:contacts')
    api_client.delete(url)
    response = api_client.get(url,
                              format='json')
    assert response.status_code == 201


def test_put_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.put(
        url,
        data={
            'email':  'New@gmail.com',
            'title': 'NewTitle',
            'text': 'NewText'
        },
        format='json'
    )
    assert response.status_code == 200


def test_patch_contact(api_client, user):
    contact_id = Contact.objects.last().id
    url = reverse('api-currency:contact', kwargs={'pk': contact_id})
    response = api_client.patch(
        url,
        data={
            'title': 'NewTitle',
            'text': 'NewText'
        },
        format='json'
    )
    assert response.status_code == 200


class Response:
    pass


def test_task_privat(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {"ccy": "USD", "base_ccy": "UAH", "buy": "27.10", "sale": "27.43"},
            {"ccy": "EUR", "base_ccy": "UAH", "buy": "29.20", "sale": "29.75"},
            {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.32", "sale": "0.35"}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    Rate.objects.all().delete()

    _privat()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.10')
    assert rate[0].sale == Decimal('27.43')
    assert rate[0].source == 1
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.20')
    assert rate[1].sale == Decimal('29.75')
    assert rate[1].source == 1
    Rate.objects.all().delete()


def test_task_mono(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {"currencyCodeA": 840, "currencyCodeB": 980, "rateBuy": 27.25, "rateSell": 27.51},
            {"currencyCodeA": 978, "currencyCodeB": 980, "rateBuy": 29.45, "rateSell": 29.83},
            {"currencyCodeA": 643, "currencyCodeB": 980, "rateBuy": 0.315, "rateSell": 0.36}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.25')
    assert rate[0].sale == Decimal('27.51')
    assert rate[0].source == 2
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.45')
    assert rate[1].sale == Decimal('29.83')
    assert rate[1].source == 2
    Rate.objects.all().delete()
