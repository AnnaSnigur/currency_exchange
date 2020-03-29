from django.db import models
from django.contrib.auth.models import AbstractUser
from src import model_choices as mch
from uuid import uuid4


def avatar_path(instance, filename: str) -> str:
    # ext = filename.split('.')[-1]
    # f = str(uuid4())
    # filename = f'{f}.{ext}'
    # return '/'.join(['hello', filename])

    return '/'.join(['avatar', str(instance.id), str(uuid4()), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = User.objects.get(pk=self.pk)
            if old_self.avatar and self.avatar != old_self.avatar:
                old_self.avatar.delete(False)
        return super(User, self).save(*args, **kwargs)


class Rate(models.Model):
    currency = models.PositiveIntegerField(choices=mch.CURRENCY_CHOICES)
    source = models.PositiveIntegerField(choices=mch.SOURCE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.created}{self.get_currency_display()}{self.sale}{self.buy}'


class Contact(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=150)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
