from django.shortcuts import render, get_object_or_404


from .models import Car
def detail(request, id):
    car = get_object_or_404(Car, pk=id)
    date = car.overview_date + timedelta(days=365)
    print(date)
    return render(request, "cars/detail.html", {"car": car})

def cars(request):
    return render(request, "cars/cars.html",
                  {"cars": Car.objects.all()})