from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if "@" not in self.email:
            raise ValueError("Invalid email address")
        super().save(*args, **kwargs)
    
    class Meta:
        db_table= "Users"

