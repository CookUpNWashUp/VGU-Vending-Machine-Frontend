from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone

# Create your models here.
class Price(models.Model):
    price = models.IntegerField(default=10000, unique=True)

    def __str__(self):
        return str(self.price)
    def get_absolute_url(self):
        return reverse('pricetag',args=[str(self.id)])

class Discount(models.Model):
    discountAmount = models.FloatField(default=0)
    discountExpired = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=1),null=True,blank=True)
    #discountCreated= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.discountAmount)

    def get_absolute_url(self):
        return reverse('discount-detail', args=[str(self.id)])

    def stil_valid(self):
        return self.Expired <= timezone.now()

class Product(models.Model):
    productName= models.CharField(max_length=50, help_text='Product Name')
    price = models.ForeignKey(Price, on_delete = models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete = models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.productName

    def get_absolute_url(self):
        return reverse('product-detail',args=[str(self.id)])

#The slot to pin dictionary will be hardwired in settings.py
class Slot(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    slotNr = models.IntegerField(default=0,unique=True)
    quantity = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse('slot', args=[str(self.id)])

    def __str__(self):
        return str(self.product.productName + '-' + str(self.slotNr))
