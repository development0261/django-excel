import email
from multiprocessing import AuthenticationError
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth import login,logout,authenticate
from .forms import userform
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


def userlogin(request):
    if request.method == 'POST':
        print("456")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                # print("123")
                login(request,user)
                return redirect('view')

            else:
                return HttpResponse("inactive user")

        else:
            return HttpResponse("Incorrect credentials")

    else:
        return render(request,'login.html')

def register(request):
    registered=False
    

    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        #messages function
        if not User.objects.filter(username=username).exists():
            if password == confirmpassword:
                user = User.objects.create_user(username=username,password=password)
                login(request,user)
                return redirect('view')
            else:
                return redirect('register')
        else:
            return redirect('register')



    return render(request,'register.html',{'registered':registered})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def saveTableRow(request,tableName):
    if request.method == "POST":

        topic = request.POST['topic']
        author = request.POST['author']
        date = request.POST['date']

        if tableName == "Content_Pitching":
            tableObj = apwire_ContentPitching.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Writing_Rewrite":
            tableObj = apwire_WritingRewrite.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Review_Draft_1":
            tableObj = apwire_ReviewDraft1.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Review_Draft_2":
            tableObj = apwire_ReviewDraft2.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
        
        if tableName == "FDN_Approval_1":
            tableObj = apwire_FDNApproval.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Ready_For_Release":
            tableObj = apwire_ReadyForRelease.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "App_Published":
            tableObj = apwire_APPublished.objects.create(topic = topic,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

def getRowData(request,id,tableName):
    
    tableObj = Blog.objects.get(pk = id)
    date = tableObj.date
    formatedDate = date.strftime('%Y-%m-%d')
    # image = tableObj.image
    return JsonResponse({'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':tableObj.image.url})

def editBlog(request,pk):
    if request.method == 'POST':
        print(pk)
        blog = Blog.objects.filter(pk=pk).update(id=pk,topic=request.POST['topic'],author=request.user,description=request.POST['description'])
        # blog = Blog.objects.update(id=pk,topic=request.POST['topic'],author=request.user,description=request.POST['description'])
        if 'image' in request.FILES:
            image=request.POST['image']
            blog.image = image
            blog.save()
        return redirect('view')
    return render(request,'editblog.html')  

@csrf_exempt
def editData(request,id,tableName):
    topic = request.POST['topic']
    description = request.POST['description']
 
    
    tableObj = Blog.objects.get(pk = id)
    
    tableObj.description = description
    tableObj.topic = topic
    tableObj.save()

    date = datetime.strptime(str(tableObj.date), '%Y-%m-%d')

    formatedDate = date.strftime('%B %d,%Y')
    return JsonResponse({'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk})



def viewfunction(request):
    # qs1 = models.apwire_ContentPitching.objects.get(id=1)
    # context_dict= {}
    # for i in qs1:
    #     context_dict['topic'] = qs1.topic
    #     context_dict['topic'] = qs1.topic
    #     context_dict['topic'] = qs1.topic

    # userobj = User.objects.get(username=request.user)
    # roleint = userdata(user=userobj).accessint
    # print(roleint)

    if request.user.is_authenticated:
        apwire_ContentPitching_data = Blog.objects.filter(status='Content_Pitching') 
        apwire_WritingRewrite_data = Blog.objects.filter(status='Writing_Rewrite')
        apwire_ReviewDraft1_data = Blog.objects.filter(status='Review_Draft_1')
        apwire_ReviewDraft2_data = Blog.objects.filter(status='Review_Draft_2')
        apwire_FDNApproval_data = Blog.objects.filter(status='FDN_Approval_1')
        apwire_ReadyForRelease_data = Blog.objects.filter(status='Ready_For_Release')
        apwire_APPublished_data = Blog.objects.filter(status='App_Published')
        context_dict = {}
        context_dict['Content Pitching'] = apwire_ContentPitching_data
        context_dict['Writing Rewrite'] = apwire_WritingRewrite_data
        context_dict['Review Draft 1'] = apwire_ReviewDraft1_data
        context_dict['Review Draft 2'] = apwire_ReviewDraft2_data
        context_dict['FDN Approval 1'] = apwire_FDNApproval_data
        context_dict['Ready For Release'] = apwire_ReadyForRelease_data
        context_dict['App Published'] = apwire_APPublished_data

        return render(request,'index.html',{'context_dict':context_dict})
    else:
        return redirect('loginview')

def createBlog(request):
    if request.method == 'POST':
        Blog.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description'],image=request.FILES['image'],status="Content_Pitching")
        return redirect('view')
    return render(request,'createBlog.html')



@csrf_exempt
def dropData(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)

        roles = request.user.get_table_role()
        print(roles[addedto])
        blog = Blog.objects.get(pk=dropid)
        blog.status= addedto
        blog.save()

        key_list = list(roles.keys())
        index = key_list.index(addedto)

        return JsonResponse({'msg':'success','role':roles[addedto],'tableIndex':index+1})
    

def logout_view(request):
    logout(request)
    return redirect('loginview')

# Publisher: All steps - view/ edit/ move/ upload
# Admin: view/ edit
# Writer1: step 1 - view/ edit/ move/
# Writer2: step 2 - view/ edit/ move/
# Writer3: step 1 - view/ edit/ move/
# Editor: all steps - view/ edit/ move/

# # Add validation for admin on move 

# - Create View Button Beside Edit (No any Conditions applied on it)
# - AddUnique Id ViewBlog_{{key|.....}}
# - Add Same class to all ViewBlog
# - Click event on ViewBlog
# - Create Single New Model same as Add Blog and make body empty(also give id)
# - Retrive data from backend as we doing for editview and append data in modal body 