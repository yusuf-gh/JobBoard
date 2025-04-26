from Apps.common.functions import user_directory_path
from django.db import models
from Apps.common.models import BaseModel
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser, BaseModel):
    is_employer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    blank=True,
                                    null=True)
    date_joined = None # переопределение что-бы избежать повторения
    verification_code = models.CharField(max_length=5,
                                         blank=True,
                                         null=True)  # Поле для кода
    def clean(self):
        # валидация номера телефона
        if self.phone_number:
            if not re.match(r'^\+?[1-9]\d{1,14}$', self.phone_number):
                raise ValidationError("Неверный формат номера телефона. Номер должен быть в международном формате.")

    def save(self, *args, **kwargs):
        self.full_clean()  # вызывает clean() + проверку всех полей модели
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"



class AplicantProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Соискатель')
    bio = models.TextField(max_length=2000,
                           blank=True,
                           null=True)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    resume = models.FileField(upload_to=user_directory_path)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    photo = models.ImageField(upload_to=user_directory_path)
    skills = ArrayField(models.CharField(max_length=100),
                                 blank=True,
                                 default=list)
    location = models.CharField() # временно Charfield позже будет заменен на географическое поле

    def __str__(self):
        return self.user



class EmployerProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Работодатель')
    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True,
                              null=True,
                              verbose_name='Вэб-сайт')
    description = models.TextField(max_length=2000,
                                   blank=True,
                                   null=True)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    logo = models.ImageField(upload_to=user_directory_path)
    location = models.CharField()  # временно Charfield позже будет заменен на географическое поле

    def __str__(self):
        return self.user



class BlankResume(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Соискатель')
    title = models.CharField(max_length=255,
                             help_text="Желаемая должность")
    bio = models.TextField(blank=True,
                           null=True,
                           help_text="Кратко о себе")
    location = models.CharField()  # временно Charfield позже будет заменен на географическое поле
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Фото')


    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def phone_number(self):
        return f"{self.user.phone_number}"

    @property
    def email(self):
        return f"{self.user.email}"




