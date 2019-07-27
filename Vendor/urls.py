from django.urls import path
from . import views

urlpatterns = [
    path('getData/<idList>', views.dataReplication,name='dataEntryReplication'),
    path('getData', views.dataReplication,name='dataReplication'),
    path('test/<int:slotNumber>', views.querytest,name='querytest'),
    path('', views.index,name='index'),
]
