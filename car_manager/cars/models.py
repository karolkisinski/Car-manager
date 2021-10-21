from django.db import models

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Driver {self.first_name} {self.last_name}"

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    overview_date = models.DateField()
    oil_change_date = models.DateField()
    driver= models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} - {self.model}"

