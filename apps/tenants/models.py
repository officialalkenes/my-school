from django.contrib.auth import get_user_model

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class SchoolOwner(TenantMixin):
    school_name = models.CharField(max_length=100)
    name = models.CharField(
        max_length=100, unique=True, verbose_name=_("School Short Name")
    )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True)
    country = models.CharField(max_length=20, default="Nigeria")
    state = models.CharField(max_length=100, verbose_name=_("State In Nigeria"))
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass
