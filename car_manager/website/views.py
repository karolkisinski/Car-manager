from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from cars.models import Car
def welcome(request):
    return render(request, "website/welcome.html",
                  {"num_cars": Car.objects.count()})
def date(request):
    return HttpResponse("This page was served at " + str(datetime.now()))