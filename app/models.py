import datetime

from django.db import models


class Saloon(models.Model):
    saloon_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=20, null=False)
    open_time = models.TimeField()
    close_time = models.TimeField()
    number_of_seats = models.IntegerField(default=1)


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    time_taken = models.IntegerField(default=15)


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    saloon_id = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=datetime.datetime.now())
    start_time = models.TimeField()
    end_time = models.TimeField()
