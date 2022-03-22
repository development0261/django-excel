import email
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

        title = request.POST['title']
        author = request.POST['author']
        date = request.POST['date']

        if tableName == "Content_Pitching":
            tableObj = apwire_ContentPitching.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Writing_Rewrite":
            tableObj = apwire_WritingRewrite.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Review_Draft_1":
            tableObj = apwire_ReviewDraft1.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Review_Draft_2":
            tableObj = apwire_ReviewDraft2.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
        
        if tableName == "FDN_Approval_1":
            tableObj = apwire_FDNApproval.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "Ready_For_Release":
            tableObj = apwire_ReadyForRelease.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        if tableName == "App_Published":
            tableObj = apwire_APPublished.objects.create(title = title,author = author,Date = date)
            date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
            formatedDate = date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

def getRowData(request,id,tableName):
    if tableName == "Content_Pitching":
        tableObj = apwire_ContentPitching.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Writing_Rewrite":
        tableObj = apwire_WritingRewrite.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Review_Draft_1":
        tableObj = apwire_ReviewDraft1.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Review_Draft_2":
        tableObj = apwire_ReviewDraft2.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "FDN_Approval_1":
        tableObj = apwire_FDNApproval.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Ready_For_Release":
        tableObj = apwire_ReadyForRelease.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "App_Published":
        tableObj = apwire_APPublished.objects.get(pk = id)
        date = tableObj.Date
        formatedDate = date.strftime('%Y-%m-%d')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
        

@csrf_exempt
def editData(request,id,tableName):
    title = request.POST['title']
    author = request.POST['author']
    date = request.POST['date']
    if tableName == "Content_Pitching":
        tableObj = apwire_ContentPitching.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Writing_Rewrite":
        tableObj = apwire_WritingRewrite.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "Review_Draft_1":
        tableObj = apwire_ReviewDraft1.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
    
    if tableName == "Review_Draft_2":
        tableObj = apwire_ReviewDraft2.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

    if tableName == "FDN_Approval_1":
        tableObj = apwire_FDNApproval.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
    
    if tableName == "Ready_For_Release":
        tableObj = apwire_ReadyForRelease.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
    
    if tableName == "App_Published":
        tableObj = apwire_APPublished.objects.get(pk = id)
        tableObj.Date = date
        tableObj.author = author
        tableObj.title = title
        tableObj.save()

        date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
        formatedDate = date.strftime('%B %d,%Y')
        return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})


def viewfunction(request):
    # qs1 = models.apwire_ContentPitching.objects.get(id=1)
    # context_dict= {}
    # for i in qs1:
    #     context_dict['Title'] = qs1.title
    #     context_dict['Title'] = qs1.title
    #     context_dict['Title'] = qs1.title

    # userobj = User.objects.get(username=request.user)
    # roleint = userdata(user=userobj).accessint
    # print(roleint)

    apwire_ContentPitching_data = apwire_ContentPitching.objects.all() 
    apwire_WritingRewrite_data = apwire_WritingRewrite.objects.all()
    apwire_ReviewDraft1_data = apwire_ReviewDraft1.objects.all()
    apwire_ReviewDraft2_data = apwire_ReviewDraft2.objects.all()
    apwire_FDNApproval_data = apwire_FDNApproval.objects.all()
    apwire_ReadyForRelease_data = apwire_ReadyForRelease.objects.all()
    apwire_APPublished_data = apwire_APPublished.objects.all()
    context_dict = {}
    context_dict['Content Pitching'] = apwire_ContentPitching_data
    context_dict['Writing Rewrite'] = apwire_WritingRewrite_data
    context_dict['Review Draft 1'] = apwire_ReviewDraft1_data
    context_dict['Review Draft 2'] = apwire_ReviewDraft2_data
    context_dict['FDN Approval 1'] = apwire_FDNApproval_data
    context_dict['Ready For Release'] = apwire_ReadyForRelease_data
    context_dict['App Published'] = apwire_APPublished_data

    return render(request,'index.html',{'context_dict':context_dict})



@csrf_exempt
def dropData(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)

        if removedfrom == "Content_Pitching" and addedto=="Writing_Rewrite":
            cpobj = apwire_ContentPitching.objects.get(pk = int(dropid))
            tableObj = apwire_WritingRewrite.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_ContentPitching.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        elif removedfrom == "Writing_Rewrite" and addedto=="Review_Draft_1":
            cpobj = apwire_WritingRewrite.objects.get(pk = int(dropid))
            tableObj = apwire_ReviewDraft1.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_WritingRewrite.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        elif removedfrom == "Review_Draft_1" and addedto=="Review_Draft_2":
            cpobj = apwire_ReviewDraft1.objects.get(pk = int(dropid))
            tableObj = apwire_ReviewDraft2.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_ReviewDraft1.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        elif removedfrom == "Review_Draft_2" and addedto=="FDN_Approval_1":
            cpobj = apwire_ReviewDraft2.objects.get(pk = int(dropid))
            tableObj = apwire_FDNApproval.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_ReviewDraft2.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        elif removedfrom == "FDN_Approval_1" and addedto=="Ready_For_Release":
            cpobj = apwire_FDNApproval.objects.get(pk = int(dropid))
            tableObj = apwire_ReadyForRelease.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_FDNApproval.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

        elif removedfrom == "Ready_For_Release" and addedto=="App_Published":
            cpobj = apwire_ReadyForRelease.objects.get(pk = int(dropid))
            tableObj = apwire_APPublished.objects.create(title = cpobj.title,author = cpobj.author,Date = cpobj.Date)
            apwire_ReadyForRelease.objects.get(pk = int(dropid)).delete()
            
            formatedDate = tableObj.Date.strftime('%B %d,%Y')
            return JsonResponse({'title':tableObj.title,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})




    

def logout_view(request):
    logout(request)
    return redirect('loginview')
