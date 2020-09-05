import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField('email address', blank=False, null=False,
                              db_index=True, unique=True)

    def save(self, *args, **kwargs):
        created = not self.id
        if created:
            self.username = str(uuid.uuid4())

        super().save(*args, **kwargs)
