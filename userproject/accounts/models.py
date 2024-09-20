from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs) -> "UserAccount":
        if not email:
            raise ValueError("The email field must be set")
        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    accounts = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label: str):
        return True

    @property
    def is_staff(self):
        return self.is_admin
