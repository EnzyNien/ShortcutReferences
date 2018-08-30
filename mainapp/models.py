
from urllib.parse import urlparse
import zlib

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ShortcutRef(models.Model):

    MIN_mf = 1
    MAX_mf = 10

    real_url = models.URLField(
        verbose_name='Реальная ссылка',
        blank=False,
        null=False)

    short_url = models.URLField(
        verbose_name='Короткая ссылка',
        blank=False,
        null=False)

    add_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        editable=False,
        blank=False)

    max_following = models.PositiveIntegerField(
        verbose_name='Количество переходов',
        default=5,
        blank=True,
        null=True,)

    active = models.BooleanField(
        verbose_name='активность',
        default=True,
        blank=False)

    @staticmethod
    def create_short_url(url):
        return hex(zlib.crc32(url.encode()) & 0xffffffff)

    @property
    def get_the_remaining_transitions(self):
        transitions = ReferencesToLinks.objects.filter(parent=self).count()
        return 0 if transitions > self.max_following else self.max_following - transitions

    def get_short_url_full(self, absolute_uri):
        parse = urlparse(absolute_uri)
        return parse.scheme + "://" + parse.hostname + ":" + \
            str(parse.port) + "/" + 'shortcut' + "/" + self.short_url

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = ShortcutRef.create_short_url(self.real_url)
        super(ShortcutRef, self).save(*args, **kwargs)

    def __str__(self):
        return self.real_url

    class Meta:
        ordering = ['-add_date', 'real_url']
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class ReferencesToLinks(models.Model):

    parent = models.ForeignKey(
        ShortcutRef,
        verbose_name='Родитель',
        on_delete=models.CASCADE,
        blank=True,
        null=True,)

    add_date = models.DateTimeField(
        verbose_name='Дата обращения',
        auto_now_add=True,
        editable=False,
        blank=False)

    ip = models.GenericIPAddressField(
        blank=True,
        null=True)

    user_agent = models.CharField(
        blank=True,
        max_length=100)

    def __str__(self):
        return self.ip + "_" + str(self.add_date)

    class Meta:
        ordering = ['-add_date']
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'
