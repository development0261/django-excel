
from django.urls import path
from . import views

urlpatterns = [
    path('apnews_instance/',views.apnews_published,name='apnews_instance'),

    

]
