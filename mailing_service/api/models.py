import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Mailing(models.Model):
    date_start = models.DateTimeField(verbose_name='Start mailing date')
    time_start = models.TimeField(verbose_name='Start mailing time')
    date_end = models.DateTimeField(verbose_name='End mailing date')
    time_end = models.TimeField(verbose_name='End mailing time')
    text = models.TextField(verbose_name='Message text')
    number_code = models.CharField(
        verbose_name='Mobile operator code',
        max_length=3,
        blank=True
        )
    tag = models.CharField(
        verbose_name='filter tag',
        blank=True,
        max_length=20
    )

    @property
    def ready_to_send(self):
        now = timezone.now()
        if self.date_start <= now <= self.date_end:
            return True
        else:
            return False

    def __str__(self):
        return f'Mailing {self.id} from date {self.date_start}'

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'


class Client(models.Model):
    TIMEZONE = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_number_validator = RegexValidator(
        regex=r'^7\d{10}$',
        message='Enter a correct phone number'
    )
    phone_number = models.CharField(
        verbose_name='phone_number',
        validators=[phone_number_validator],
        max_length=11,
        unique=True
    )
    phone_number_code = models.CharField(
        verbose_name='Mobile operator code',
        max_length=3
    )
    tag = models.CharField(
        verbose_name='tag',
        blank=True,
        max_length=20
    )
    timezone = models.CharField(
        verbose_name='Time zone',
        max_length=32,
        choices=TIMEZONE,
        default='UTC'
    )

    def save(self, *args, **kwargs):
        self.phone_number_code = self.phone_number[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Client {self.id}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    SENT = 'sent'
    NO_SENT = 'no sent'

    STATUS_CHOICE = [
        (SENT, 'Sent'),
        (NO_SENT, 'No sent'),
    ]
    time_create = models.DateTimeField(
        verbose_name='Time create',
        auto_now_add=True
    )
    sending_status = models.CharField(
        verbose_name='Sending status',
        max_length=20,
        choices=STATUS_CHOICE
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='messages')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def __str__(self):
        return f'Message {self.id} with text{self.mailing} for {self.client}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = "Messages"
