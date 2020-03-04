from django.db import models
from django.contrib.auth.models import AbstractUser
from src import model_choices as mch

class User(AbstractUser):
    pass


class Rate(models.Model):
    currency = models.PositiveIntegerField(choices=mch.CURRENCY_CHOICES)
    source = models.PositiveIntegerField(choices=mch.SOURCE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.created}{self.get_currency_display()}{self.sale}{self.buy}'