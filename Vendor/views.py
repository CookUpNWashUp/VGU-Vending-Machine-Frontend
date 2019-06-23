from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
from .models import Product,Slot
from django.http import HttpResponse
from .forms import Order
from django.conf import settings
import json
from .dispense import dispense

# Create your views here.

#BACKEND_API_URL='http://192.168.1.121:8000/hello'

def index(request):
    if (request.method == 'GET'):
        slots = Slot.objects.order_by('slotNr')
        initialValues = {'amount':0}
        form = Order(initial=initialValues)
        context = {'form':form,'slots':slots}
    elif (request.method == 'POST'):
        form = Order(request.POST)
        if form.is_valid():
            try:
                auth = HTTPBasicAuth(form.cleaned_data['username'],form.cleaned_data['password'])
                r = requests.get(settings.BACKEND_API_URL, auth = auth)
                if (r.status_code == 200):
                    apiRep = r.content
                    jsonData = json.loads(apiRep.decode('ascii'))
                    status = jsonData['status']
                    if(status == 1):
                        status = 'Failed - Insufficient Fund'
                    elif(status == 0):
                        #orderedSlot = get_object_or_404(Slot,slotNr=form.cleaned_data['slotNr'])
                        #orderedSlot.quantity = orderedSlot.quantity - form.cleaned_data['amount']
                        for i in range(form.cleaned_data['amount']):
                            dispense(form.cleaned_data['slot'])
                        status = 'OK'
                elif (r.status_code == 401):
                    status = 'Failed - 401'
            except:
                status = 'Failed - Many things can cause this'
            context ={'status': status}
    return render(request, 'storepage.html',context)


