from django.contrib import admin
from django.urls import path , re_path , include
from . import views

urlpatterns = [

    re_path("^$", views.index, name='index'),
    
    path('admin/', admin.site.urls),
]
