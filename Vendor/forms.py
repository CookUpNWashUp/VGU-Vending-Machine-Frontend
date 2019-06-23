from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class Order(forms.Form):
    #querySet = Product.objects.all()
    #product = forms.ModelChoiceField(querySet, to_field_name='productName')
    amount = forms.IntegerField(help_text='how many?')
    slot = forms.IntegerField(help_text='which slot?')
    #need to look up how many chars are supported in the user model
    username = forms.CharField(max_length=50,strip=True)
    password = forms.CharField(max_length=50,strip=True)

    def clean_username(self):
        #No validations yet, to be added later
        data = self.cleaned_data['username']
        return data
    def clean_password(self):
        #No validations yet, to be added later
        data = self.cleaned_data['password']
        return data
    def clean_amount(self):
        #No validations yet, to be added later
        data = self.cleaned_data['amount']
        return data
    def clean_slot(self):
        #If slot number exceeds 26 the form should return an error
        data = self.cleaned_data['slot']
        return data
