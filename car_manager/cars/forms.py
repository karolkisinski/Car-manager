from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Car, Driver


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'overview_date', 'oil_change_date', 'driver']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.none()
        self.fields['overview_date'] = forms.CharField(
            widget=forms.DateInput(attrs={'class': 'form-control col-md-4', 'type': 'date'}))
        self.fields['oil_change_date'] = forms.CharField(
            widget=forms.DateInput(attrs={'class': 'form-control col-md-4', 'type': 'date'}))
        if user_id is not None:
            # update queryset for exercise field
            self.fields['driver'].queryset = Driver.objects.filter(user_id=user_id)
        # self.fields['driver'] = forms.ModelChoiceField(queryset=Driver.objects.filter(user_id=user_id))
        else:
            # UserExercises.objects.none() will return an empty queryset
            self.fields['driver'].queryset = Driver.objects.none()

    # driver = forms.ModelChoiceField(queryset=Driver.objects.none())


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'phone', 'email']
        exclude = ['car_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),

        }