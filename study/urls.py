from django.contrib import admin
from django.urls import path , re_path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    re_path("^$", views.index, name='index'),
    path("accounts/", include('accounts.urls')),
    path("accounts/", include("allauth.urls")),


    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)