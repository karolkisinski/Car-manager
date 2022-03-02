from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #car = models.ForeignKey(Car, default=1, on_delete=models.SET_DEFAULT)


    def __str__(self):
        return f"Driver {self.first_name} {self.last_name}"

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    overview_date = models.DateField()
    oil_change_date = models.DateField()
    driver = models.ForeignKey(Driver, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def overview_next_date(self):
        return (self.overview_date + timedelta(days=365))

    def __str__(self):
        return f"{self.brand} - {self.model}"

