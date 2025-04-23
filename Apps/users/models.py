from django.db import models
from Apps.common.models import BaseModel
import re
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

class User(BaseModel):

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=255)

    is_employer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    blank=True,
                                    null=True
                                    )
    verification_code = models.CharField(max_length=5,
                                         blank=True,
                                         null=True
                                         )  # Поле для кода

    def clean(self):
        # валидация номера телефона
        if self.phone_number:
            if re.match(r'^\+?[1-9]\d{1,14}$', self.phone_number):
                return
            else:
                raise ValidationError("Неверный формат номера телефона. Номер должен быть в международном формате.")
        super().clean()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        while True:
            new_id = get_random_string(length=6, allowed_chars='0123456789')
            if not User.objects.filter(id=new_id).exists():
                return new_id

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"