from django import forms
from .models import Product,Slot
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

AMOUNT_ERROR = 'Don\'t waste our time buying nothing'
SLOT_ERROR = 'Don\'t waste your time ordering a slot having nothing'

class Order(forms.Form):
    #querySet = Product.objects.all()
    #product = forms.ModelChoiceField(querySet, to_field_name='productName')
    #amount = forms.IntegerField(help_text='how many?')
    #slot = forms.IntegerField(help_text='which slot?')
    amount = forms.IntegerField()
    slot = forms.IntegerField(min_value=0,max_value=27)
    #need to look up how many chars are supported in the user model
    #username = forms.CharField(max_length=50,strip=True,widget=forms.TextInput(attrs={'id':'username'}))
    username = forms.CharField(max_length=50,strip=True,widget=forms.HiddenInput)
    password = forms.CharField(required=False,max_length=50,strip=True,widget=forms.PasswordInput)
    token  = forms.CharField(max_length=6,strip=True,widget=forms.HiddenInput,required=True)

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
        if (data<=0):
            raise ValidationError(_(AMOUNT_ERROR))
        return data
    def clean_slot(self):
        #If slot number exceeds 26 the form should return an error
        data = self.cleaned_data['slot']
        try:
            slot = Slot.objects.get(slotNr__exact=data)
        except Slot.DoesNotExist:
            raise ValidationError(_(SLOT_ERROR))
        return data
    def clean_token(self):
        #No validations yet, to be added later
        data = self.cleaned_data['token']
        return data
