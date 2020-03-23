from jsonfield import JSONField

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField('Email address', unique=True)
    phone = models.CharField(verbose_name='Phone', max_length=50, blank=True, null=True)
    address = JSONField(verbose_name='Address', blank=True, null=True, default={})

    last_update = models.DateTimeField(verbose_name='Last update', blank=True, null=True)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    @property
    def full_name(self):
        return self.get_full_name()
