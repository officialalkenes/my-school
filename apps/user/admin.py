from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": ("email", "password", "user_type", "admission_number"),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Groups"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = (
        "id",
        "user_type",
        "email",
        "is_staff",
        "last_login",
    )
    list_display_links = (
        "id",
        "user_type",
        "email",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)
