from django.db import models

import subscriptions.models
import users.models
from utils.validators import validate_phone_number
from users.models import CustomUser
from subscriptions.models import Package

class Gateway(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='gateways/')
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = [
        (STATUS_VOID, 'void'),
        (STATUS_PAID, 'paid'),
        (STATUS_ERROR, 'error'),
        (STATUS_CANCELED, 'User Canceled'),
        (STATUS_REFUNDED, 'Refunded'),

    ]

    STATUS_TRANSLATIONS = {
        STATUS_VOID: 'Payment could not be processed',
        STATUS_PAID: 'Payment successful',
        STATUS_ERROR: 'Payment has encountered and error.',
        STATUS_CANCELED: 'Payment canceled by user',
        STATUS_REFUNDED: 'this payment has been refunded',
    }

    user = models.ForeignKey(users.models.CustomUser, verbose_name='user', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey(subscriptions.models.Package, verbose_name='package', related_name='%(class)s', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, verbose_name='gateway', related_name='%(class)s', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_VOID)
    device_uuid = models.CharField(max_length=40, blank=True)
    # token = models.CharField(max_length=20)
    phone_number = models.BigIntegerField(validators=[validate_phone_number])
    consumed_code = models.PositiveIntegerField(null=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'




