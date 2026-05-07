from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        ANALYST = 'analyst', 'Analyst'
        VIEWER = 'viewer', 'Viewer'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=24, choices=Role.choices, default=Role.ANALYST)
    workspace_id = models.CharField(max_length=36, blank=True, default='')
    api_rate_limit = models.PositiveIntegerField(default=1000)

    def __str__(self) -> str:
        return self.email or self.username
