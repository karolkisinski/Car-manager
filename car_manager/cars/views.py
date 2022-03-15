from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CarForm, DriverForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *

from .models import Car, Driver


def detail(request, id):
    car = get_object_or_404(Car, pk=id)
    date = car.overview_date + timedelta(days=365)
    return render(request, "cars/detail.html", {"car": car})


def cars(request):
    pk = request.GET.get('pk')
    form = CarForm(user_id=request.user.id)
    if request.method == 'POST':
        form = CarForm(request.POST, user_id=request.user.id)
        if form.is_valid():
            form.save()
    context = {'form': form}
    user = request.user
    return render(request, "cars/cars.html",
                  {"cars": Car.objects.filter(user_id=user.id),
                   "form": form,
                   "drivers_count": Driver.objects.filter(user_id=user.id).count(),
                   "cars_count": Car.objects.filter(user_id=user.id).count()})

def drivers(request):
    pk = request.GET.get('pk')
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    user = request.user
    return render(request, "cars/drivers.html",
                  {"drivers": Driver.objects.filter(user_id=user.id),
                   "form": form,
                   "drivers_count": Driver.objects.filter(user_id=user.id).count()})

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Owner')
            user.groups.add(group)
            messages.success(request, "Account was created for " + username)
            return redirect('login')
    context = {'form':form}
    return render(request, "accounts/register.html", context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username OR password is incorrect")
    context = {}
    return render(request, "accounts/login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
#@owner_only
def home(request):
    user = request.user
    return render(request, "website/home.html", {"cars": Car.objects.filter(user_id=user.id)})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Driver'])

def driver(request):
    context = {}
    return render(request, 'website/driver.html', context)

@login_required(login_url='login')
#@owner_only
def createCar(request):
    user = request.user
    form = CarForm(user_id = user.id)
    if request.method == 'POST':
        form = CarForm(request.POST, user_id=request.user.id)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('cars')
    context = {'form': form}
    return render(request, 'cars/car_form.html', context)

@login_required(login_url='login')
#@owner_only
def createDriver(request):
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            return redirect('drivers')
    context = {'form': form}
    return render(request, 'cars/driver_form.html', context)

@login_required(login_url='login')
#@owner_only
def updateCar(request, pk):
    car = Car.objects.get(id=pk)
    form = CarForm(instance=car, user_id=request.user.id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car, user_id=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('cars')
    context = {'form': form}
    return render(request, 'cars/car_form.html', context)

@login_required(login_url='login')
#@owner_only
def deleteCar(request, pk):
    car = Car.objects.get(pk=pk)
    car.delete()
    context = {}
    return redirect('cars')

@login_required(login_url='login')
#@owner_only
def updateDriver(request, pk):
    driver = Driver.objects.get(id=pk)
    form = DriverForm(instance=driver)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('drivers')
    context = {'form': form}
    return render(request, 'cars/driver_form.html', context)

@login_required(login_url='login')
#@owner_only
def deleteDriver(request, pk):
    driver = Driver.objects.get(pk=pk)
    driver.delete()
    context = {}
    return redirect('drivers')
