from django.urls import path, include
from . import views

app_name = "EpochGrail"

urlpatterns = [
    path('', views.index, name='index'),
    path('item_list', views.view_item_list, name="item_list")
]