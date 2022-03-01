from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Car, Driver

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, Driver):
#         """ Customises the labels for checkboxes"""
#         return "%s" % Driver.name

class CarForm(ModelForm):
    # def __init(self, *args, **kwargs):
    #     #self.request = kwargs.pop('request')
    #     super(CarForm, self).__init__(*args, **kwargs)
    #     self.fields['driver'].queryset = Driver.objects.all().filter(
    #         user_id=self.request.user.id
    #     )
    class Meta:
        model = Car
        fields = ['brand', 'model', 'overview_date', 'oil_change_date', 'driver']
    brand = forms.CharField()
    model = forms.CharField()
    overview_date = forms.DateInput()
    oil_change_date = forms.DateInput()
    # driver = CustomModelMultipleChoiceField(
    #     queryset=Driver.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(CarForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            # update queryset for exercise field
            self.fields['driver'].queryset = Driver.objects.filter(user=user_id)
        else:
            # UserExercises.objects.none() will return an empty queryset
            self.fields['driver'].queryset = Driver.objects.none()
    driver = forms.ModelChoiceField(queryset=Driver.objects.none())

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ['user']
