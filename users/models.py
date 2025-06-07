from django.db import models

class User(models.Model):

    countries = [("US", "USA"),
                 ("FR", "France"),
                 ("DE", "Germany")]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    age = models.IntegerField()
    rating = models.FloatField(default=0.0, blank=True)
    country = models.CharField(choices=countries, default="DE", help_text="Where are you from?")

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info")
    maried = models.BooleanField()


class Actor(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor, related_name="movies")

