from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
options = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError("email is required ")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.BigIntegerField(unique=True, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=options, null=True)
    created_on = models.DateField(auto_now_add=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ('created_on',)
        verbose_name = 'Users'

    def __str__(self):
        return self.username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'dob', 'gender']

    def __str__(self):
        return self.username
