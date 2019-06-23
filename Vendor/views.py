from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
from .models import Product
from django.http import HttpResponse
from .forms import Order

# Create your views here.

BACKEND_API_URL='http://192.168.1.121:8000/hello'

def index(request):
    if (request.method == 'GET'):
        products = Product.objects.order_by('id')
        initialValues = {'amount':0}
        form = Order(initial=initialValues)
        context = {'form':form,'products':products}
    elif (request.method == 'POST'):
        form = Order(request.POST)
        if form.is_valid():
            auth = HTTPBasicAuth(form.cleaned_data['username'],form.cleaned_data['password'])
            r = requests.get(BACKEND_API_URL, auth = auth)
            #Check for the status here
            #Add a JSON parser
            #Add low level code to control GPIO
            status = str(r.content)
            context ={'status':status}
    return render(request, 'storepage.html',context)


