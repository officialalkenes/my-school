from django.contrib.auth.models import PermissionsMixin, BaseUserManager


class Manager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password):
        ...

    def create_superuser(self, email, firstname, lastname, password):
        ...
