from django.db import models
from Apps.common.models import BaseModel
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):

    is_employer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    blank=True,
                                    null=True
                                    )

    date_joined = None # переопределение что-бы избежать повторения

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

    def __str__(self):
        return f"{self.username}"



class Profile(models.Model):

    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,
                             verbose_name="пользователь"
                             )
    bio = models.TextField(max_length=2000,
                           blank=True,
                           null=True
                           )

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.user.id, filename)

    resume = models.FileField(upload_to=user_directory_path)

