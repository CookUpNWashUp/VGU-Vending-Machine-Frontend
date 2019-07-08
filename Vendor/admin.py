from django.contrib import admin
from Vendor.models import Discount, Product, Price, Slot
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Register your models here.
# Once Master-Slave replication has been setup, local admin will lose control over
# Product and Price.
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(Price)
#admin.site.register(Slot)

SLOT_ERROR='This slot is reserved for hardware and is not available'
SLOT_LIST_CONFIGURATION = ('slotNr', 'product', 'quantity')

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['slotNr','product','quantity']

    def clean(self):
        slotNr = self.cleaned_data['slotNr']
        if slotNr in settings.NFC_PIN_MAPPING:
            raise forms.ValidationError(_(SLOT_ERROR))
        return self.cleaned_data

class SlotAdmin(admin.ModelAdmin):
    form = SlotForm
    list_display = SLOT_LIST_CONFIGURATION

admin.site.register(Slot,SlotAdmin)
