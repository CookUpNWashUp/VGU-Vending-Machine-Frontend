from django.urls import path
from . import views

urlpatterns = [
    path('test/<int:slotNumber>', views.querytest,name='querytest'),
    path('', views.index,name='index'),
]
