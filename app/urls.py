from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewfunction,name='view'),
    path('view2',views.viewfunction2,name='view2'),
    path('login',views.userlogin,name='loginview'),
    # path('logfail',views.logfail,name='logfail'),
    path('register',views.register,name='register'),
    path('createBlog',views.createBlog,name='createBlog'),
    path('editBlog/<str:pk>/',views.editBlog,name='editBlog'),

    path('createBlog2',views.createBlog2,name='createBlog2'),

    path('saveTableRow/<str:tableName>/',views.saveTableRow,name="saveTableRow"),
    path('getRowData/<int:id>/<str:tableName>/',views.getRowData,name="getRowData"),
    path('viewgetRowData/<int:id>/<str:tableName>/',views.getRowData,name="getRowData"),
    path('editData/<int:id>/<str:tableName>/',views.editData,name="editData"),
    path('draganddrop/<int:dropid>/<str:removedfrom>/<str:addedto>/',views.dropData,name="dropData"),
    path('logout',views.logout_view,name='logout'),

    path('viewgetRowData2/<int:id>/<str:tableName>/',views.getRowData2,name="getRowData2"),
    path('getRowData2/<int:id>/<str:tableName>/',views.getRowData2,name="getRowData2"),
    path('editData2/<int:id>/<str:tableName>/',views.editData2,name="editData2"),
    path('draganddrop2/<int:dropid>/<str:removedfrom>/<str:addedto>/',views.dropData2,name="dropData2"),


]