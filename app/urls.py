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

    path('publishBlog/<str:pk>/',views.publishBlog,name='publishBlog'),
    path('publishBlog2/<str:pk>/',views.publishBlog2,name='publishBlog2'),

    path('downloadxmlall/',views.downloadxmlall,name='downloadxmlall'),
    path('downloadxmlall2/',views.downloadxmlall2,name='downloadxmlall2'),
    path('downloadxmlallfile2/',views.downloadxmlallfile2,name='downloadxmlallfile2'),
    path('downloadxmlall2file2/',views.downloadxmlall2file2,name='downloadxmlall2file2'),

    path('downloadxml/<str:pk>/',views.downloadxml,name='downloadxml'),
    path('downloadxml2/<str:pk>/',views.downloadxml2,name='downloadxml2'),

    path('downloadpdf/<str:pk>/',views.downloadpdf,name='downloadpdf'),
    path('downloadpdf2/<str:pk>/',views.downloadpdf2,name='downloadpdf2'),

    path('downloadxmlfile2/<str:pk>/',views.downloadxmlfile2,name='downloadxmlfile2'),
    path('downloadxml2file2/<str:pk>/',views.downloadxml2file2,name='downloadxml2file2'),
    path('downloadxmlallfile2/<str:pk>/',views.downloadxmlallfile2,name='downloadxmlallfile2'),
    path('downloadxml2allfile2/<str:pk>/',views.downloadxmlall2file2,name='downloadxml2allfile2'),

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