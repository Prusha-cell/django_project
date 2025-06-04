from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Autor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    profile = models.URLField(null=True, blank=True,
                              verbose_name="Ссылка на страницу автора")
    deleted = models.BooleanField(default=False,
                                  help_text="Был ли удален автор из БД авторов?")
    rating = models.IntegerField(default=1,
            validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
library/models.py
