from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    blood_group = models.CharField(max_length=5)


class SerialData(models.Model):

    data = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)


class Data(models.Model):
    bpm = models.DecimalField(max_digits=5, decimal_places=2)
    cardiac_output = models.DecimalField(max_digits=5, decimal_places=2)
    stroke_volume = models.DecimalField(max_digits=5, decimal_places=2)
    estimated_delta = models.DecimalField(max_digits=5, decimal_places=2)
    stiffness_index = models.DecimalField(max_digits=10, decimal_places=2)
    augmented_index = models.DecimalField(max_digits=5, decimal_places=2)
    pulse_wave_velocity = models.DecimalField(max_digits=5, decimal_places=4)
    plot = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Endpoint_Check(models.Model):
    status = models.BooleanField(default=False)
    user = models.IntegerField()