from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewfunction,name='view'),
    path('login',views.userlogin,name='loginview'),
    path('register',views.register,name='register'),
    path('saveTableRow/<str:tableName>/',views.saveTableRow,name="saveTableRow"),
    path('getRowData/<int:id>/<str:tableName>/',views.getRowData,name="getRowData"),
    path('editData/<int:id>/<str:tableName>/',views.editData,name="editData"),
    path('draganddrop/<int:dropid>/<str:removedfrom>/<str:addedto>/',views.dropData,name="dropData"),
    path('logout',views.logout_view,name='logout'),


]