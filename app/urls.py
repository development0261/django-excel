from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewfunction,name='view'),
    path('login',views.userlogin,name='loginview'),
    # path('logfail',views.logfail,name='logfail'),
    path('register',views.register,name='register'),
    path('createBlog',views.createBlog,name='createBlog'),
    path('editBlog/<str:pk>/',views.editBlog,name='editBlog'),

    path('get_permissions',views.get_permissions,name='get_permissions'),

    path('publishBlog/<str:pk>/',views.publishBlog,name='publishBlog'),
    path('publishBlog2/<str:pk>/',views.publishBlog2,name='publishBlog2'),

    path('backblog/<str:pk>/',views.backblog,name='backblog'),
    path('backblog2/<str:pk>/',views.backblog2,name='backblog2'),

    path('downloadxmlall/',views.downloadxmlall,name='downloadxmlall'),
    path('downloadxmlall2file2/',views.downloadxmlall2file2,name='downloadxmlall2file2'),

    path('downloadxml/<str:pk>/',views.downloadxml,name='downloadxml'),
    

    path('deleteBlog/<str:pk>/',views.deleteBlog,name='deleteBlog'),
    path('deleteBlog2/<str:pk>/',views.deleteBlog2,name='deleteBlog2'),

    path('downloadpdf/<str:pk>/',views.downloadpdf,name='downloadpdf'),
    path('downloadpdf2/<str:pk>/',views.downloadpdf2,name='downloadpdf2'),

    path('viewxmlall/',views.viewxmlall,name='viewxmlall'),
    path('viewxmlall2/',views.viewxmlall2,name='viewxmlall2'),

    path('downloadxml2file2/<str:pk>/',views.downloadxml2file2,name='downloadxml2file2'),
    
    path('downloadxml2allfile2/<str:pk>/',views.downloadxmlall2file2,name='downloadxml2allfile2'),

    path('createBlog2',views.createBlog2,name='createBlog2'),

    # path('saveTableRow/<str:tableName>/',views.saveTableRow,name="saveTableRow"),
    path('getRowData/<int:id>/<str:tableName>/',views.getRowData,name="getRowData"),
    path('viewgetRowData/<int:id>/<str:tableName>/',views.getRowData,name="getRowData"),
    path('editData/<int:id>/<str:tableName>/',views.editData,name="editData"),
    path('draganddrop/<int:dropid>/<str:removedfrom>/<str:addedto>/',views.dropData,name="dropData"),
    path('logout',views.logout_view,name='logout'),

    path('viewgetRowData2/<int:id>/<str:tableName>/',views.getRowData2,name="getRowData2"),
    path('getRowData2/<int:id>/<str:tableName>/',views.getRowData2,name="getRowData2"),
    path('editData2/<int:id>/<str:tableName>/',views.editData2,name="editData2"),
    path('draganddrop2/<int:dropid>/<str:removedfrom>/<str:addedto>/',views.dropData2,name="dropData2"),

    path('contentgetRowData',views.contentgetRowData,name="contentgetRowData"),




]