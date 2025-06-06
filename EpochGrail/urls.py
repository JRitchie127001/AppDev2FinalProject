from django.urls import path, include
from . import views

app_name = "EpochGrail"

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('create_grail', views.create_grail, name='create_grail'),
    path('edit_grail', views.edit_grail, name="edit_grail"),
    path('update_grail', views.update_grail, name='update_grail'),
    path('public_grails', views.grail_list, name='public_grails'),
    path('view_grail/<int:id>', views.view_grail, name="view_grail")
]