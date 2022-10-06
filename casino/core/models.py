from uuid import uuid4
from django.db import models


class UserDetail(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    credit = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField()

    def save(self, *args, **kwargs) -> None:
        if not self.uuid:
            self.uuid = uuid4().__str__()
        return super(UserDetail, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Symbols(models.Model):
    symbol = models.CharField(max_length=100)
    represent = models.CharField(max_length=50)
    reward = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.symbol} - {self.represent}"
