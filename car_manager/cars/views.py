from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CarForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *

from .models import Car


def detail(request, id):
    car = get_object_or_404(Car, pk=id)
    date = car.overview_date + timedelta(days=365)
    return render(request, "cars/detail.html", {"car": car})

def cars(request):
    return render(request, "cars/cars.html",
                  {"cars": Car.objects.all()})

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
@owner_only
def home(request):
    #context = {}
    cars = Car.objects.count()
    return render(request, "website/home.html", {"num_cars": cars})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Driver'])

def driver(request):
    context = {}
    return render(request, 'website/driver.html', context)

@login_required(login_url='login')
@owner_only
def createCar(request):
    form = CarForm()
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'cars/car_form.html', context)

@login_required(login_url='login')
@owner_only
def updateCar(request, pk):
    car = Car.objects.get(id=pk)
    form = CarForm(instance=car)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'cars/car_form.html', context)

@login_required(login_url='login')
@owner_only
def deleteCar(request, pk):
    car = Car.objects.get(pk=pk)
    car.delete()
    context = {}
    return redirect('cars')
