import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# User model extending Django's AbstractUser to use UUID as primary key
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
