import os

from django.db import models

from to_do_list.core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    telegram_user_id = models.CharField(max_length=100, unique=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    verification_code = models.CharField(max_length=50, default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'tg пользователь'
        verbose_name_plural = 'tg пользователи'

    @staticmethod
    def _generate_verification_code():
        return os.urandom(12).hex()

    def set_verification_code(self):
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code',))

        return code
