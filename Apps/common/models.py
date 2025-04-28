from django.db import models
import re
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

class BaseModel(models.Model):
    # Замена стандартного автоинкрементного ID на собственное поле
    id = models.CharField(max_length=6,
                          unique=True,
                          primary_key=True,
                          editable=False
                          )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super().save(*args, **kwargs)

    @classmethod
    def generate_unique_id(cls):
        while True:
            new_id = get_random_string(length=6, allowed_chars='0123456789')
            if not cls.objects.filter(id=new_id).exists():
                return new_id

    class Meta:
        abstract = True