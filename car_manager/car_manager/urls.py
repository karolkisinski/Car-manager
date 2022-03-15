"""car_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from website.views import *
from cars.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', home, name="home"),
    path('date', date),
    path('cars/<int:id>', detail),
    path('cars/cars.html', cars, name="cars"),
    path('cars/drivers.html', drivers, name="drivers"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('register/', registerPage, name="register"),
    path('create_car/', createCar, name="create_car"),
    path('create_driver/', createDriver, name="create_driver"),
    path('cars/update_car/<str:pk>/', updateCar, name="update_car"),
    path('cars/delete_car/<str:pk>/', deleteCar, name="delete_car"),
    path('cars/update_driver/<str:pk>/', updateDriver, name="update_driver"),
    path('cars/delete_driver/<str:pk>/', deleteDriver, name="delete_driver"),
    path('driver/', driver, name="driver"),
    path('password_reset', password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path('account', account, name="account"),
    path('account/change_password', change_password, name="change_password"),
]
