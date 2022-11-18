from django.db import models

import payments.models
import users.models
from utils.validators import validate_sku

from users.models import *



class Package(models.Model):
    title = models.CharField(max_length=30)
    sku = models.CharField(help_text=
                           "stock keeping unit",
                           db_index=True,
                           max_length=20, validators=[validate_sku])
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='packages/')
    is_enable = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    duration = models.DurationField(blank=True, null=True)
    # gateways = models.ManyToManyField(payments.models.Gateway)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(users.models.CustomUser, related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'





