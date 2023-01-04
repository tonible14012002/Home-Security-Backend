from django.urls import path
from django.shortcuts import render

def realtime(request):
    return render(request, 'chat.html')

urlpatterns = [
    path('', realtime)
]