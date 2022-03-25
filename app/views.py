from multiprocessing import AuthenticationError
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

# from app.serializers import BlogSerializer
from .models import *
from django.contrib.auth import login,logout,authenticate
from .forms import userform
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()


def userlogin(request):
    if request.method == 'POST':
        # print("456")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                # print("123")
                login(request,user)
                return redirect('view')

            else:
                messages.error(request, 'user is inactive') 
                return redirect('loginview')

        else:
            messages.error(request, 'Please check your password!!!') 
            return redirect('loginview')

    else:
        return render(request,'login.html')

# def logfail(req):
#     return render(req,'logfail.html')



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
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
    return JsonResponse({'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj})

def getRowData2(request,id,tableName):
    
    tableObj = Blog2.objects.get(pk = id)
    date = tableObj.date
    formatedDate = date.strftime('%Y-%m-%d')
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
    return JsonResponse({'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj})


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

@csrf_exempt
def editData2(request,id,tableName):
    topic = request.POST['topic']
    description = request.POST['description']
 
    
    tableObj = Blog2.objects.get(pk = id)
    
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


        apnews_ContentPitching_data = Blog2.objects.filter(status='Content_Pitching') 
        apnews_WritingRewrite_data = Blog2.objects.filter(status='Writing_Rewrite')
        apnews_ReviewDraft1_data = Blog2.objects.filter(status='Review_Draft_1')
        apnews_ReviewDraft2_data = Blog2.objects.filter(status='Review_Draft_2')
        apnews_FDNApproval_data = Blog2.objects.filter(status='FDN_Approval_1')
        apnews_ReadyForRelease_data = Blog2.objects.filter(status='Ready_For_Release')
        apnews_APPublished_data = Blog2.objects.filter(status='App_Published')
        context_dict1 = {}
        context_dict1['Content Pitching'] = apnews_ContentPitching_data
        context_dict1['Writing Rewrite'] = apnews_WritingRewrite_data
        context_dict1['Review Draft 1'] = apnews_ReviewDraft1_data
        context_dict1['Review Draft 2'] = apnews_ReviewDraft2_data
        context_dict1['FDN Approval 1'] = apnews_FDNApproval_data
        context_dict1['Ready For Release'] = apnews_ReadyForRelease_data
        context_dict1['App Published'] = apnews_APPublished_data




        return render(request,'index.html',{'context_dict':context_dict,'context_dict1':context_dict1})
    else:
        return redirect('loginview')

def viewfunction2(request):
    
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
      
        return render(request,'index.html',{'context_dict2':context_dict})
    else:
        return redirect('loginview')

from django.core import serializers
from django.core.files import File
import xml.etree.ElementTree as et
from datetime import datetime

def publishBlog(request,pk):
    blogobj = Blog.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.publishedon = datetime.today().date()
    blogobj.save()
    
    # data = serializers.serialize("xml", Blog.objects.filter(pk=pk))    
    # f = open('log.xml', 'w')
    # myfile = File(f)
    # myfile.write(data)
    # myfile.close()
    # root = et.Element("feed")

    # root.appendChild(xml)
    
    # entry = root.createElement('feed')
    # et.Element('xmlns:apnm', 'http://ap.org/schemas/03/2005/apnm')
    # et.Element('xmlns:apxh', 'http://w3.org/1999/xhtml')
    # et.Element('xmlns:ap', 'http://ap.org/schemas/03/2005/aptypes')
    # et.Element('xmlns', 'http://www.w3.org/2005/Atom')
    # et.Element('xmlns:apcm', 'http://ap.org/schemas/03/2005/apcm')
    # et.Element('xml:lang', 'en-us')

    # m1 = et.Element(blogobj.topic)


    
    # xml_str = root.toprettyxml(indent ="\t") 
    
    # save_path_file = "log.xml"
    
    

    # with open(save_path_file, "w") as f:
    #     f.write(xml_str) 

    data = 'xmlns:apnm="http://ap.org/schemas/03/2005/apnm" xmlns:apxh="http://w3.org/1999/xhtml" xmlns:ap="http://ap.org/schemas/03/2005/aptypes" xmlns="http://www.w3.org/2005/Atom" xmlns:apcm="http://ap.org/schemas/03/2005/apcm" xml:lang="en-us"'

    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","http://w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://www.w3.org/2005/Atom")
    root.set("xml:lang","en-us")

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "ShaktiCoin"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://draftblog.shakticoin.com//"
    a3 = root.SubElement('id')
    a3.text = "shakticoin123"
    a4 = root.SubElement('title')
    a4.text = "ShaktiCoin"
    
    # para = et.SubElement()
    # et.SubElement(para, "link", id="2", type="external", url="http://www.google.com").text="Google.com"

    a6 = root.SubElement('rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = root.SubElement('updated')
    a7.text = "2022-03-19T01:58:31Z"

    m2 = et.Element('entry')
    root.append (m1)

    
      
    b1 = et.SubElement(m2, "id")
    b1.text = str(blogobj.id)
    b2 = et.SubElement(m2, "topic")
    b2.text = str(blogobj.topic)
    b3 = et.SubElement(m2, "author")
    b3.text = str(blogobj.author)
    b3 = et.SubElement(m2, "description")
    b3.text = str(blogobj.description)
    b4 = et.SubElement(m2, "image")
    b4.text = str(blogobj.image)
    b5 = et.SubElement(m2, "date")
    b5.text = str(blogobj.date)
    b5 = et.SubElement(m2, "status")
    b5.text = str(blogobj.status)
    b5 = et.SubElement(m2, "publishedon")
    b5.text = str(blogobj.publishedon)

    # blogall = Blog.objects.filter(status="App_Published")
    # for i in blogall:
    #     m2 = et.Element('entry')
    #     root.append (m2)
    #     b1 = et.SubElement(m2, "id")
    #     b1.text = str(i.id)
    #     b2 = et.SubElement(m2, "topic")
    #     b2.text = str(i.topic)
    #     b3 = et.SubElement(m2, "author")
    #     b3.text = str(i.author)
    #     b3 = et.SubElement(m2, "description")
    #     b3.text = str(i.description)
    #     b4 = et.SubElement(m2, "image")
    #     b4.text = str(i.image)
    #     b5 = et.SubElement(m2, "date")
    #     b5.text = str(i.date)
    #     b5 = et.SubElement(m2, "status")
    #     b5.text = str(i.status)
    #     b5 = et.SubElement(m2, "publishedon")
    #     b5.text = str(i.publishedon)

    
      
    tree = et.ElementTree(root)
      
    with open ('log.xml', "wb") as files :
        tree.write(files)
  
    # Driver Code
    if __name__ == "__main__": 
        GenerateXML("log.xml")
    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))
    return redirect('view')

def publishBlog2(request,pk):
    blogobj = Blog2.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.publishedon = datetime.today().date()
    blogobj.save()

    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))
    return redirect('view')
# class toxml(APIView):
    
#     def get(self, request):
#         obj = Blog.objects.get()
#         serialize = BlogSerializer(obj,many=True)
#         return Response(serialize.data)


def createBlog(request):
    print("Createblog")
    if request.method == 'POST':
        blog = Blog.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description'],status="Content_Pitching")
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()
        return redirect('view')

    return render(request,'createBlog.html')

def createBlog2(request):
    print("Createblog2")
    if request.method == 'POST':
        blog = Blog2.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description2'],status="Content_Pitching")
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()
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


@csrf_exempt
def dropData2(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)

        roles = request.user.get_table_role()
        print(roles[addedto])
        blog = Blog2.objects.get(pk=dropid)
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