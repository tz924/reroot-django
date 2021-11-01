from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    education = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)


class City(models.Model):
    name = models.CharField(max_length=64)
    population = models.IntegerField()
    state = models.CharField(max_length=2)
    comparison = models.ForeignKey(
        "Comparison", related_name="cities", blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="favorites",
                             blank=True, null=True, on_delete=models.CASCADE)
    longitude = models.CharField(
        verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(
        verbose_name="Latitude", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Submission(models.Model):
    user = models.ForeignKey(User, related_name="submissions",
                             blank=True, null=True, on_delete=models.CASCADE)


class Comparison(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comparisons",
                             blank=True, null=True, on_delete=models.CASCADE)
