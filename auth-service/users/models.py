from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, mpesa_phone, password=None, **extra_fields):
        if not mpesa_phone:
            raise ValueError('The MPESA phone number must be set')
        user = self.model(mpesa_phone=mpesa_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mpesa_phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(mpesa_phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    mpesa_phone = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'mpesa_phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mpesa_phone
