from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
import requests
from requests.auth import HTTPBasicAuth
from .models import Product,Slot
from django.http import HttpResponse,JsonResponse
from .forms import Order
from django.conf import settings
import json
from .dispense import dispense
from django.db import IntegrityError

# Create your views here.

#BACKEND_API_URL='http://192.168.1.121:8000/hello'

SUCCESS = 'You ordered {} {} from slot #{}. Your balance is {}' 
ERROR_INSUFFICIENT_FUND = 'Failed - Insufficient Fund'
ERROR_INSUFFICIENT_QUANTITY = 'Failed - Insufficient Quantity'
ERROR_WRONG_CREDS = 'Failed - Username or token is invalid'
ERROR_NO_PRODUCT = 'Failed - Product not found'
ERROR_BACKEND = 'Failed - 401'
ERROR_OTHERS = 'Failed - Many things can cause this'
ERROR_DUMB = 'Don\'t waste your time buying nothing'

def index(request):
    if (request.method == 'GET'):
        slots = Slot.objects.filter(quantity__gt=0).order_by('slotNr')
        form = Order()
        context = {'form':form,'slots':slots}
    elif (request.method == 'POST'):
        form = Order(request.POST)
        if form.is_valid():
            try:
                orderedSlot = get_object_or_404(Slot,slotNr__exact=form.cleaned_data['slot'])
                #Form json for the request here
                reqData = {
                            'userId':form.cleaned_data['username'],
                            'token':form.cleaned_data['token'],
                            'deviceId':settings.MACHINE_ID,
                            'productIds':[{
                                'productId':orderedSlot.product.productId,
                                'amount':form.cleaned_data['amount']
                             }]
                        }
                reqJSON = json.dumps(reqData)
                print(reqJSON)
                headers = {'Content-Type':'application/json'}
                #Make the requrest
                #auth = HTTPBasicAuth(form.cleaned_data['username'],form.cleaned_data['password'])
                r = requests.post(settings.BACKEND_TRANSACTION_API_URL, headers=headers,data=reqJSON)
                if (r.status_code == 200):
                    apiRep = r.content
                    jsonData = json.loads(apiRep.decode('ascii'))['data']
                    print(jsonData)
                    status = jsonData['TransactionStatus']
                    if(status == 1):
                        status = ERROR_INSUFFICIENT_FUND
                    elif(status == 2):
                        status = ERROR_WRONG_CREDS
                    elif(status == 3):
                        status = ERROR_NO_PRODUCT
                    elif(status == 0):
                        #orderedSlot = get_object_or_404(Slot,slotNr__exact=form.cleaned_data['slot'])
                        if (orderedSlot.quantity >= form.cleaned_data['amount']):
                            orderedSlot.quantity = orderedSlot.quantity - form.cleaned_data['amount']
                            '''for i in range(form.cleaned_data['amount']):
                                dispense(form.cleaned_data['slot'])'''
                            status = SUCCESS.format(str(form.cleaned_data['amount']),orderedSlot.product.productName,str(orderedSlot.slotNr),jsonData['balance'])
                            orderedSlot.save()
                        else:
                            status = ERROR_INSUFFICIENT_QUANTITY
                elif (r.status_code == 401 or r.status_code == 404):
                    status = ERROR_BACKEND
                else:
                    status = r.status_code
            except:
                status = ERROR_OTHERS
                #raise
            #context ={'status': status}
            #return status
        else:
            status=form.errors
            #print(form.errors['slot'])
        context ={'status': status}
    return render(request, 'storepage.html',context)

def querytest(request, slotNumber):
    #inventory = Slot.objects.get(slotNr__exact=2)
    inventory = get_object_or_404(Slot,slotNr__exact=slotNumber)
    return HttpResponse('{}'.format(inventory.quantity))

def dataReplication(request,idList=[]):
    #Get the data from backend API
    reqData = {
                'machine_id': settings.MACHINE_ID,
                'product_ids': idList,
            }
    reqJSON = json.dumps(reqData)
    headers = {'Content-Type':'application/json'}
    r = requests.get(settings.BACKEND_DATA_API_URL, headers=headers,data=reqJSON)
    #Parse data to database
    if (r.status_code == 200):
        code = r.status_code
        apiRep = r.content
        #This load has already converted all jsons in the array to dict
        jsonData = json.loads(apiRep.decode('ascii'))['data']
        #Error handling for invalid machine
        if ('APIStatus' in jsonData):
            code=500
            return HttpResponse(code)
        for entry in jsonData:
            try:
                product = Product.objects.get(productId=entry['id'])
                product.productName = entry['product_name']
                product.price = entry['price']
                product.save()
            except Product.DoesNotExist as e:
                try:
                    newEntry = Product(productId=entry['id'],productName=entry['product_name'],price=entry['price'])
                    newEntry.save()
                except IntegrityError as e:
                    #code=e.__cause__
                    code = 500 
    return HttpResponse(code)
