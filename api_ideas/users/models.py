from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
