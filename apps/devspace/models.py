from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from apps.devspace.utils import generate_keys

User = get_user_model()


class DevAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, verbose_name=_("API KEY"), blank=True)
    secret_key = models.CharField(
        max_length=40, verbose_name=_("SECRET API KEY"), blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.key}"

    def save(self, *args, **kwargs):
        if not self.secret_key:
            keys = generate_keys()
            self.key = keys[0]
            self.secret_key = keys[1]
        return super().save(args, kwargs)
