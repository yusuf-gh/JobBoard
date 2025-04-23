from django.db import models

class BaseModel(models.Model):
    # Замена стандартного автоинкрементного ID на собственное поле
    id = models.CharField(max_length=6,
                          unique=True,
                          primary_key=True,
                          editable=False
                          )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True