from django.urls import path
from . import views

urlpatterns = [
    path('notify-visit/', views.new_visit),
]