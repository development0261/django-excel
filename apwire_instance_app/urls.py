

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apwire_instance_app import views


urlpatterns = [
    path('apwire_instance/',views.apwire_published,name="apwire_instance" ),
    path('login_instance/',views.login_instance,name='login_instance'),
    path('register_instance/',views.register_instance,name='register_instance'),
    path('logout_instance/',views.logout_instance,name='logout_instance')

]