from django import forms
from django.contrib.auth.models import User
from shop.models import UserProfile, UserClass


class Register_ApplicationForm(forms.Form):
    business_name = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    contact_person = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)



