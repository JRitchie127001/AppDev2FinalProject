from django.urls import path, include
from . import views

app_name = "EpochGrail"

urlpatterns = [
    path('', views.index, name='index'),
]