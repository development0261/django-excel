import os
import random,string    
from itertools import count
from multiprocessing import AuthenticationError
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from soupsieve import select

# from app.serializers import BlogSerializer
from .models import *
from django.contrib.auth import login,logout,authenticate
from .forms import userform
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()

from bs4 import BeautifulSoup as bs
import re
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from django.core import serializers
from django.core.files import File
import xml.etree.ElementTree as et
from datetime import datetime
from wsgiref.util import FileWrapper

from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image, Frame

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from PIL import Image
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT


from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image, Frame

def xmlfolder_exist():
    xmlfolder_exist = os.path.exists(MEDIA_ROOT+"/xml")
    print(xmlfolder_exist)
    
    if not xmlfolder_exist:
        os.makedirs(MEDIA_ROOT+"/xml")

def pdffolder_exist():
    pdffolder_exist = os.path.exists(MEDIA_ROOT+"/pdf")
    print(pdffolder_exist)
    
    if not pdffolder_exist:
        os.makedirs(MEDIA_ROOT+"/pdf")


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)
        if not User.objects.filter(username=username).exists():
            messages.warning(request, f'User with username "{username}" does not exist') 
            return redirect('viewfunction')
        elif User.objects.filter(username=username).exists():
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('viewfunction')

                else:
                    messages.error(request, 'user is inactive') 
                    return redirect('viewfunction')

            else:
                messages.warning(request, 'Incorrect Password') 
                return redirect('viewfunction')
        else:
            return redirect('viewfunction')

    else:
        return render(request,'login.html')

# def logfail(req):
#     return render(req,'logfail.html')

def get_permissions(request):
    try:
        user_obj = permissions.objects.get(user=request.user)
        return render(request,'index.html',{'obj':user_obj})
    except:
        return HttpResponse("permissions object does not exist")
    

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
                return redirect('viewfunction')
            else:
                messages.warning(request,"Passwords don't match")
                return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.warning(request,"This user already exists")
            return redirect('register')
    else:
        return render(request,'register.html',{'registered':registered})


# @csrf_exempt
# def saveTableRow(request,tableName):
#     if request.method == "POST":

#         topic = request.POST['topic']
#         author = request.POST['author']
#         date = request.POST['date']

#         if tableName == "Content_Pitching":
#             tableObj = apwire_ContentPitching.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

#         if tableName == "Writing_Rewrite":
#             tableObj = apwire_WritingRewrite.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

#         if tableName == "Review_Draft_1":
#             tableObj = apwire_ReviewDraft1.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

#         if tableName == "Review_Draft_2":
#             tableObj = apwire_ReviewDraft2.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})
        
#         if tableName == "FDN_Approval_1":
#             tableObj = apwire_FDNApproval.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

#         if tableName == "Ready_For_Release":
#             tableObj = apwire_ReadyForRelease.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

#         if tableName == "App_Published":
#             tableObj = apwire_APPublished.objects.create(topic = topic,author = author,Date = date)
#             date = datetime.strptime(tableObj.Date, '%Y-%m-%d')
#             formatedDate = date.strftime('%B %d,%Y')
#             return JsonResponse({'topic':tableObj.topic,'author':tableObj.author,'date':formatedDate,'pk':tableObj.pk})

def getRowData(request,id,tableName):
    current_user = request.user.username
    tableObj = Ap_Wire.objects.get(pk = id)
    if current_user == tableObj.author.username:
        current_user_check = True
    else:
        current_user_check = False

    if request.user.is_superuser:
        superuser_check = True
    else:
        superuser_check = False

    date = tableObj.date
    formatedDate = date.strftime('%d %b %y')
    # image = tableObj.image
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
    imageobjs = moreimages_apwire.objects.filter(post = tableObj)
    imgdict = {}
    if not imageobjs:
        pass
    else:
        count = 0
        for i in imageobjs:
            count += 1
            imgdict[str(count)]=i.image.url
    

    blog_progress_status = tableObj.blog_release_status
    if tableObj.category:
        category_name = tableObj.category.name
    else:
        category_name = None
    return JsonResponse({'status':tableObj.blog_release_status,'superuser_check':superuser_check,'current_user_check':current_user_check,'category':category_name,'blog_progress_status':blog_progress_status,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj,'imgdict':imgdict})

@csrf_exempt
def contentgetRowData(request):
    return JsonResponse({})

@csrf_exempt
def contentgetRowData2(request):
    return JsonResponse({})

def getRowData2(request,id,tableName):
    current_user = request.user.username
    tableObj = Ap_News.objects.get(pk = id)
    if current_user == tableObj.author.username:
        current_user_check = True
    else:
        current_user_check = False

    if request.user.is_superuser:
        superuser_check = True
    else:
        superuser_check = False
    date = tableObj.date
    formatedDate = date.strftime('%d %b %y')
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
    imageobjs = moreimages_apnews.objects.filter(post = tableObj)
    imgdict = {}
    if not imageobjs:
        pass
    else:
        count = 0
        for i in imageobjs:
            count += 1
            imgdict[str(count)]=i.image.url
    
    if tableObj.category:
        category_name = tableObj.category.name
    else:
        category_name = None

    return JsonResponse({'status':tableObj.blog_release_status,'superuser_check':superuser_check,'current_user_check':current_user_check,'category':category_name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj,'imgdict':imgdict})

def editBlog(request,pk):
    if request.method == 'POST':
        print(request.POST['dropdown'])
        blog = Ap_Wire.objects.filter(pk=pk).update(topic=request.POST['topic'],author=request.user,description=request.POST['description'],category=request.POST['dropdown'])
        
        blog.save()
        print("called")
        if 'image' in request.FILES:
            image=request.POST['image']
            blog.image = image
            blog.save()
        
        

        return redirect('viewfunction')
    return render(request,'editblog.html')  



@csrf_exempt
def editData(request,id,tableName):
    current_user = request.user.username
    topic = request.POST['topic']
    description = request.POST['description']
    cat_id = request.POST['category']
    author_id = request.POST['author']
    
    
    blog_progress_status = request.POST['status']
    print(blog_progress_status)
    tableObj = Ap_Wire.objects.get(pk = id)
    
    if cat_id == "Select Category":
        cat_obj = None
        category_name = None
    else:
        cat_obj= category.objects.get(id=cat_id)
        category_name = cat_obj.name
    

    
    tableObj.description = description
    tableObj.topic = topic
    
    #updating author
    if request.user.is_superuser:
        User = get_user_model()
        auth_update = User.objects.get(id= author_id)
        tableObj.author = auth_update
        auth_update.save()
    

    tableObj.category = cat_obj
    if current_user == tableObj.author.username or request.user.is_superuser:
        current_user_check = True
        tableObj.blog_release_status = blog_progress_status
        
    else:
        current_user_check = False
        blog_progress_status = tableObj.blog_release_status

    if request.user.is_superuser:
        superuser_check = True
    else:
        superuser_check = False
    # tableObj.blog_release_status = category.objects.get(id=cat_id)
    tableObj.save()
    
    if 'image' in request.FILES:
        image=request.FILES['image']
        tableObj.image = image
        tableObj.save()
        del request.FILES['image']
    
    count = 0
    if f'image{count}' in request.FILES:    
        moreimages_apwire.objects.filter(post=tableObj).delete()
        for i in request.FILES:
            moreimages_apwire.objects.create(post=tableObj,image=request.FILES[f'image{count}'])
            count += 1

    date = datetime.strptime(str(tableObj.date), '%Y-%m-%d')
    
    # desc  length
    desc = tableObj.description
    desc = desc.replace("&nbsp;","")
    desc = desc.replace("&#39;","")
    desc = re.sub('<[^<]*?/?>', '', desc)
    splitdesc = desc.split()
    formatedDate = date.strftime('%B %d,%Y')
    if not tableObj.description:
        desc_len = 0
    else:
        desc_len = len(splitdesc)
    
    temp = str(tableObj.updated)
    year_dict = {
        "01":"Jan",
        "02":"Feb",
        "03":"Mar",
        "04":"Apr",
        "05":"May",
        "06":"Jun",
        "07":"Jul",
        "08":"Aug",
        "09":"Sep",
        "10":"Oct",
        "11":"Nov",
        "12":"Dec"
    }
    month = year_dict[temp[5:7]]
    datetimevalue = temp[8:10]+" "+month+" "+temp[2:4]+" "+"-"+" "+temp[11:16]

    if permissions.objects.filter(user__in = [request.user],status=tableObj.status).exists():
        permiss = permissions.objects.filter(user = request.user,status=tableObj.status).first()
            
        access_dict = {
            'create':permiss.create ,
            'edit':permiss.edit ,
            'view':permiss.view ,
            'to_delete':permiss.to_delete ,
            'move':permiss.move,
            'publish':permiss.publish
        }

    return JsonResponse({'access_dict':access_dict,'superuser_check':superuser_check,'datetimevalue':datetimevalue,'updated':tableObj.updated,'tablename':tableObj.status,'row_id':tableObj.id,'desc_len':desc_len,'blog_progress_status':blog_progress_status,'current_user_check':current_user_check,'category':category_name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk})

@csrf_exempt
def editData2(request,id,tableName):
    current_user = request.user.username
    topic = request.POST['topic']
    description = request.POST['description']
    cat_id = request.POST['category']
    blog_progress_status = request.POST['status']
    author_id = request.POST['author']
    print(author_id)

    
    if cat_id == "Select Category":
        cat_obj = None
        category_name = None
    else:
        cat_obj= category.objects.get(id=cat_id)
        category_name = cat_obj.name
    
    
    
    

    tableObj = Ap_News.objects.get(pk = id)
    tableObj.category = cat_obj
    tableObj.description = description
    tableObj.topic = topic

    #updating author
    if request.user.is_superuser:
        User = get_user_model()
        auth_update = User.objects.get(id= author_id)
        tableObj.author = auth_update
        auth_update.save()

    if current_user == tableObj.author.username or request.user.is_superuser:
        current_user_check = True
        tableObj.blog_release_status = blog_progress_status
        
    else:
        current_user_check = False
        blog_progress_status = tableObj.blog_release_status
    
    tableObj.save()
    if 'image' in request.FILES:
        image=request.FILES['image']
        tableObj.image = image
        tableObj.save()
        del request.FILES['image']

    count = 0
    if f'image{count}' in request.FILES:    
        moreimages_apnews.objects.filter(post=tableObj).delete()
        print(request.FILES)
        for i in request.FILES:
            moreimages_apnews.objects.create(post=tableObj,image=request.FILES[f'image{count}'])
            count += 1
        

    date = datetime.strptime(str(tableObj.date), '%Y-%m-%d')

    # desc  length
    desc = tableObj.description
    desc = desc.replace("&nbsp;","")
    desc = desc.replace("&#39;","")
    desc = re.sub('<[^<]*?/?>', '', desc)
    splitdesc = desc.split()
    if not tableObj.description:
        desc_len = 0
    else:
        desc_len = len(splitdesc)

    temp = str(tableObj.updated)
    year_dict = {
        "01":"Jan",
        "02":"Feb",
        "03":"Mar",
        "04":"Apr",
        "05":"May",
        "06":"Jun",
        "07":"Jul",
        "08":"Aug",
        "09":"Sep",
        "10":"Oct",
        "11":"Nov",
        "12":"Dec"
    }
    month = year_dict[temp[5:7]]
    datetimevalue = temp[8:10]+" "+month+" "+temp[2:4]+" "+"-"+" "+temp[11:16]
    formatedDate = date.strftime('%B %d,%Y')


    if permissions.objects.filter(user__in = [request.user],status=tableObj.status).exists():
        permiss = permissions.objects.filter(user = request.user,status=tableObj.status).first()
            
        access_dict = {
            'create':permiss.create ,
            'edit':permiss.edit ,
            'view':permiss.view ,
            'to_delete':permiss.to_delete ,
            'move':permiss.move,
            'publish':permiss.publish
        }
    return JsonResponse({'access_dict':access_dict,'datetimevalue':datetimevalue,'updated':tableObj.updated,'desc_len':desc_len,'blog_progress_status':blog_progress_status,'current_user_check':current_user_check,'category':category_name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk})



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
        
        apwire_ContentPitching_data = Ap_Wire.objects.filter(status='Content_Pitching') 
        apwire_WritingRewrite_data = Ap_Wire.objects.filter(status='Writing_Rewrite')
        apwire_ReviewDraft1_data = Ap_Wire.objects.filter(status='Review_Draft_1')
        apwire_ReviewDraft2_data = Ap_Wire.objects.filter(status='Review_Draft_2')
        apwire_FDNApproval_data = Ap_Wire.objects.filter(status='FDN_Approval_1')
        apwire_ReadyForRelease_data = Ap_Wire.objects.filter(status='Ready_For_Release')
        apwire_APPublished_data = Ap_Wire.objects.filter(status='App_Published')
        context_dict = {}
        context_dict['Content Pitching'] = apwire_ContentPitching_data
        context_dict['Writing Rewrite'] = apwire_WritingRewrite_data
        context_dict['Review Draft 1'] = apwire_ReviewDraft1_data
        context_dict['Review Draft 2'] = apwire_ReviewDraft2_data
        context_dict['FDN Approval 1'] = apwire_FDNApproval_data
        context_dict['Ready For Release'] = apwire_ReadyForRelease_data
        context_dict['App Published'] = apwire_APPublished_data

        apnews_ContentPitching_data = Ap_News.objects.filter(status='Content_Pitching') 
        apnews_WritingRewrite_data = Ap_News.objects.filter(status='Writing_Rewrite')
        apnews_ReviewDraft1_data = Ap_News.objects.filter(status='Review_Draft_1')
        apnews_ReviewDraft2_data = Ap_News.objects.filter(status='Review_Draft_2')
        apnews_FDNApproval_data = Ap_News.objects.filter(status='FDN_Approval_1')
        apnews_ReadyForRelease_data = Ap_News.objects.filter(status='Ready_For_Release')
        apnews_APPublished_data = Ap_News.objects.filter(status='App_Published')
        context_dict1 = {}
        context_dict1['Content Pitching'] = apnews_ContentPitching_data
        context_dict1['Writing Rewrite'] = apnews_WritingRewrite_data
        context_dict1['Review Draft 1'] = apnews_ReviewDraft1_data
        context_dict1['Review Draft 2'] = apnews_ReviewDraft2_data
        context_dict1['FDN Approval 1'] = apnews_FDNApproval_data
        context_dict1['Ready For Release'] = apnews_ReadyForRelease_data
        context_dict1['App Published'] = apnews_APPublished_data

        
        

        

        obj = content_brief.objects.all()
        if obj:
            context = obj
        else:
            context = None
    
        permissions.objects.filter(user=request.user)

        categories = category.objects.all()


        User = get_user_model()

        users = User.objects.values()

        


        

        

        return render(request,'index.html',{'user_dict':users,'context_dict1':context_dict1,'context_dict':context_dict,'category_dict':categories,'context':context})
        
    else:        
        return redirect('loginview')




def publishBlog2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.published_on = datetime.today().date()
    blogobj.save()

    messages.success(request,"Your blog {} for AP News is Published".format(blogobj.topic))

    filepath = downloadxml(request,pk,stringPath=True)
    return redirect('/?filepath={}&secondTab=True'.format(filepath))
    

def printpdf(desc,imagepath,topic,images):
    import time
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    topic=str(topic)
    doc = SimpleDocTemplate(f"{MEDIA_ROOT}/pdf/{topic}.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18,title=f"{topic}")
    Story=[]
    if imagepath:
        im = Image(imagepath, 6*inch, 3.5*inch)
        Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = topic
    topic = topic.replace("/", "").replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("|", "").replace("?", "").replace("*", "")
    Story.append(Paragraph(ptext, styles["Title"]))       
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))
    
    for i in desc:
        ptext = i
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

    for i in images:
        Story.append(Spacer(1, 12))
        im = Image(i, 6*inch, 3.5*inch)
        Story.append(im)
    print(images)
    pdffolder_exist()
    x=doc.build(Story)
    
    response = FileResponse(open(f"{MEDIA_ROOT}/pdf/{topic}.pdf", 'rb'),as_attachment=True)
    return response

def buildxml(pk,blogobj):
    randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","https://www.w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://ap.org/schemas/03/2005/apcm")
    root.set("xml:lang","en")

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "ShaktiCoin"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://shakticoin.com/"
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    a5 = et.SubElement(root,'link')
    a5.set("href","https://ap.shakticoin.com/post-sitemap.xml")
    a5.set("rel","self")
    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    a7.text = str(utz)


    m2 = et.Element('entry')
    m2.set("xml:lang","en")
    root.append (m2)

    reverted_count=str(blogobj.reverted_count)
    if reverted_count == "None" :
        uid = "urn:publicid:ap.shakticoin:"+str(randno)+"0"
    else:
        uid = "urn:publicid:ap.shakticoin:"+str(randno)+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:]
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)
    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 
    a = et.SubElement(m2,"category")
    a.set("label","Global")
    a.set("term","Global")
    a.set("scheme","http://cv.ap.org/keyword")

    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
    elee = et.SubElement(m2,"apcm:ContentMetadata")
    elem = et.SubElement(elee,"apcm:HeadLine")
    elem.text=str(blogobj.topic)
    elem = et.SubElement(elee,"apcm:Characteristics")
    elem.set("MediaType","Text")

    elee = et.SubElement(m2,"apnm:NewsManagement")
    elem = et.SubElement(elee,"apnm:ManagementId")
    if reverted_count == "None" :
        elem.text = "urn:publicid:shakticoin:"+str(randno)+"0"
    else:
        elem.text = "urn:publicid:shakticoin:"+str(randno)+reverted_count
    elem = et.SubElement(elee,"apnm:ManagementType")
    elem.text="Change"
    elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
    elem.text="3"
    elem = et.SubElement(elee,"apnm:PublishingStatus")
    elem.text="Usable"

    m2 = et.Element('entry')
    m2.set("xml:lang","en")
    root.append (m2)

    if reverted_count == "None" :
        uid = "urn:publicid:ap.shakticoin.com:"+randno+"0"
    else:
        uid = "urn:publicid:ap.shakticoin.com:"+randno+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:]
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)

    

    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 

    images_obj = moreimages_apwire.objects.filter(post = blogobj)
    if images_obj:
        for i in images_obj:
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(i.image)) 
    
    # b1 = et.SubElement(m2, "link")
    # b1.set("rel","related")
    # if reverted_count == "None" :
    #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"0")
    # else:
    #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)

    elee = et.SubElement(m2,"apcm:ContentMetadata")
    elem = et.SubElement(elee,"apcm:HeadLine")
    elem.text=str(blogobj.topic)
    elem = et.SubElement(elee,"apcm:Characteristics")
    elem.set("MediaType","Photo")

    elee = et.SubElement(m2,"apnm:NewsManagement")
    elem = et.SubElement(elee,"apnm:ManagementId")
    if reverted_count == "None" :
        elem.text = "urn:publicid:ap.shakticoin.com:"+randno+"0"
    else:
        elem.text = "urn:publicid:shakticoin:"+randno+reverted_count
    elem = et.SubElement(elee,"apnm:ManagementType")
    elem.text="Change"
    elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
    elem.text="3"
    elem = et.SubElement(elee,"apnm:PublishingStatus")
    elem.text="Usable"
    
    
    
    
    x = blogobj.description.split("\n")
    y = []
    z=[]
    count = 0
    for i in x:
        count += 1
        if count % 2 != 0:
            y.append(i)
    for i in y:  
        i = i.replace("&nbsp;","")
        i = i.replace("&#39;","")
        z.append(i)
        soup = bs(i,'html.parser')
        results = soup.find_all('a')
        print(results)
        i = re.sub('<[^<]*?/?>', ' ', i)
        ele = et.SubElement(o1, "apxh:p")
        ele.text = str(i)
        for obj in results:
            ele1 = et.SubElement(ele,"apxh:a")
            # b2 = et.SubElement(ele, "title")
            # b2.text = ""
            ele1.set("href",str(obj['href']))
            # ele1.set("target","_blank")
            ele1.set("rel","nofollow noopener")
            ele1.text=str(obj.text)

    tree = et.ElementTree(root)

    tree2 = et.ElementTree(root)

    xmlfolder_exist()
    tree.write('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8")

    # response = FileResponse(open(f"{MEDIA_ROOT}/xml/{topic}.pdf", 'rb'),as_attachment=True)

def buildxml2(pk,blogobj):
    randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","https://www.w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://ap.org/schemas/03/2005/apcm")
    root.set("xml:lang","en")

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "ShaktiCoin"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://shakticoin.com/"
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    a5 = et.SubElement(root,'link')
    a5.set("href","https://ap.shakticoin.com/post-sitemap.xml")
    a5.set("rel","self")
    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    a7.text = str(utz)


    m2 = et.Element('entry')
    m2.set("xml:lang","en")
    root.append (m2)

    reverted_count=str(blogobj.reverted_count)
    if reverted_count == "None" :
        uid = "urn:publicid:ap.shakticoin:"+str(randno)+"0"
    else:
        uid = "urn:publicid:ap.shakticoin:"+str(randno)+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:]
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)
    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 
    a = et.SubElement(m2,"category")
    a.set("label","Global")
    a.set("term","Global")
    a.set("scheme","http://cv.ap.org/keyword")

    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
    elee = et.SubElement(m2,"apcm:ContentMetadata")
    elem = et.SubElement(elee,"apcm:HeadLine")
    elem.text=str(blogobj.topic)
    elem = et.SubElement(elee,"apcm:Characteristics")
    elem.set("MediaType","Text")

    elee = et.SubElement(m2,"apnm:NewsManagement")
    elem = et.SubElement(elee,"apnm:ManagementId")
    if reverted_count == "None" :
        elem.text = "urn:publicid:shakticoin:"+str(randno)+"0"
    else:
        elem.text = "urn:publicid:shakticoin:"+str(randno)+reverted_count
    elem = et.SubElement(elee,"apnm:ManagementType")
    elem.text="Change"
    elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
    elem.text="3"
    elem = et.SubElement(elee,"apnm:PublishingStatus")
    elem.text="Usable"

    m2 = et.Element('entry')
    m2.set("xml:lang","en")
    root.append (m2)

    if reverted_count == "None" :
        uid = "urn:publicid:ap.shakticoin.com:"+randno+"0"
    else:
        uid = "urn:publicid:ap.shakticoin.com:"+randno+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:]
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:]
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)

    

    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 

    images_obj = moreimages_apnews.objects.filter(post = blogobj)
    if images_obj:
        for i in images_obj:
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(i.image)) 
    
    # b1 = et.SubElement(m2, "link")
    # b1.set("rel","related")
    # if reverted_count == "None" :
    #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"0")
    # else:
    #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)

    elee = et.SubElement(m2,"apcm:ContentMetadata")
    elem = et.SubElement(elee,"apcm:HeadLine")
    elem.text=str(blogobj.topic)
    elem = et.SubElement(elee,"apcm:Characteristics")
    elem.set("MediaType","Photo")

    elee = et.SubElement(m2,"apnm:NewsManagement")
    elem = et.SubElement(elee,"apnm:ManagementId")
    if reverted_count == "None" :
        elem.text = "urn:publicid:ap.shakticoin.com:"+randno+"0"
    else:
        elem.text = "urn:publicid:shakticoin:"+randno+reverted_count
    elem = et.SubElement(elee,"apnm:ManagementType")
    elem.text="Change"
    elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
    elem.text="3"
    elem = et.SubElement(elee,"apnm:PublishingStatus")
    elem.text="Usable"
    
    
    
    
    x = blogobj.description.split("\n")
    y = []
    z=[]
    count = 0
    for i in x:
        count += 1
        if count % 2 != 0:
            y.append(i)
    for i in y:  
        i = i.replace("&nbsp;","")
        i = i.replace("&#39;","")
        z.append(i)
        soup = bs(i,'html.parser')
        results = soup.find_all('a')
        print(results)
        i = re.sub('<[^<]*?/?>', ' ', i)
        ele = et.SubElement(o1, "apxh:p")
        ele.text = str(i)
        for obj in results:
            ele1 = et.SubElement(ele,"apxh:a")
            # b2 = et.SubElement(ele, "title")
            # b2.text = ""
            ele1.set("href",str(obj['href']))
            # ele1.set("target","_blank")
            ele1.set("rel","nofollow noopener")
            ele1.text=str(obj.text)

    tree = et.ElementTree(root)

    tree2 = et.ElementTree(root)

    xmlfolder_exist()
    tree.write('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8",xml_declaration=True)


def downloadpdf(request,pk):
    blogobj = Ap_Wire.objects.get(pk=pk)
    imglist = []
    if blogobj.image:
        image_data = "https://shaktidjangoblog-prod.s3.amazonaws.com"+"/"+blogobj.image.name    
    else:
        image_data = None    
    if moreimages_apwire.objects.filter(post=blogobj):
        for i in moreimages_apwire.objects.filter(post=blogobj):
            imglist.append("https://shaktidjangoblog-prod.s3.amazonaws.com"+"/"+i.image.name)
    
    x = blogobj.description.split("\n")
    y = []
    z=[]
    count = 0
    for i in x:
        count += 1
        if count % 2 != 0:
            y.append(i)
    for i in y:
        i = i.replace("&nbsp;","")
        i = i.replace("&#39;","\'")
        
        
        z.append(i)
    pdf = printpdf(z,image_data,str(blogobj.topic),imglist) 
    return pdf

def downloadpdf2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    imglist = []
    if blogobj.image:
        image_data = "https://shaktidjangoblog-prod.s3.amazonaws.com"+"/"+blogobj.image.name    
    else:
        image_data = None    
    if moreimages_apnews.objects.filter(post=blogobj):
        for i in moreimages_apnews.objects.filter(post=blogobj):
            imglist.append("https://shaktidjangoblog-prod.s3.amazonaws.com"+"/"+i.image.name)
    
    x = blogobj.description.split("\n")
    y = []
    z=[]
    count = 0
    for i in x:
        count += 1
        if count % 2 != 0:
            y.append(i)
    for i in y:
        i = i.replace("&nbsp;","")
        i = i.replace("&#39;","\'")
        
        
        z.append(i)
    
    pdf = printpdf(z,image_data,str(blogobj.topic),imglist)
    return pdf



def downloadxml(request,pk,stringPath= None):
    blogobj = Ap_Wire.objects.get(pk=pk)
    response = buildxml(pk,blogobj)
    
    # Pathout is the path to the output.xml

    xmlFile = open('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')
    response['Content-Disposition'] = "attachment; filename=output_xml_Blog_AP_Wire_{}_{}.xml".format(blogobj.pk,blogobj.topic)
    
   

    if stringPath:
        return '/media/xml/output_xml_Blog_AP_Wire_{}.xml'.format(blogobj.pk)
    else:
        return response

def viewxml(request,pk):
    blogobj = Ap_Wire.objects.get(pk=pk)
    buildxml(pk,blogobj)
    response = open('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    return HttpResponse(response.read(),content_type="application/xml")

def viewxml2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    buildxml2(pk,blogobj)
    response = open('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    return HttpResponse(response.read(),content_type="application/xml")


def publishBlog(request,pk):
    blogobj = Ap_Wire.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.published_on = datetime.today().date()
    blogobj.save()
    
    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))

    filepath = downloadxml(request,pk,stringPath=True)
    return redirect('/?filepath={}'.format(filepath))

def backblog(request,pk):
    blogobj = Ap_Wire.objects.get(pk=pk)
    blogobj.status = "Content_Pitching"
    blogobj.published_on = datetime.today().date()
    blogobj.save()
    
    messages.success(request,"Your blog {} was reverted back to Content Pitching".format(blogobj.topic))


    return redirect('viewfunction')

def backblog2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    blogobj.status = "Content_Pitching"
    blogobj.published_on = datetime.today().date()
    blogobj.save()
    
    messages.success(request,"Your blog {} was reverted back to Content Pitching".format(blogobj.topic))


    return redirect('/?secondTab=True')

def downloadxml2file2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    

    buildxml2(pk,blogobj)
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')
    response['Content-Disposition'] = "attachment; filename=output_xml_Blog_AP_Wire_{}_{}.xml".format(blogobj.pk,blogobj.topic)
    
    
    return response


def buildxmlall():
    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","https://www.w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://ap.org/schemas/03/2005/apcm")
    root.set("xml:lang","en")

    

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "ShaktiCoin"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://shakticoin.com/"
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    # para = ET.SubElement(..., "p", link_id=1)
    # ET.SubElement(para, "link", id=2, type="external", url="http://www.google.com").text="Google.com"

    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"

    # current time and timezone
    now = str(datetime.now())
    now_format = now
    now_format = now[:10]+"T"+now[11:]

    from django.utils.timezone import get_current_timezone
    current_tz = get_current_timezone()


    if str(current_tz) == "UTC":
        tz_format = "00:00"

    a7 = et.SubElement(root,'updated')
    a7.text = now_format+"+"+tz_format

    

    blogall = Ap_Wire.objects.filter(Q(status="Ready_For_Release") | Q(status="App_Published"))
    for blogobj in blogall:        
        randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        m2 = et.Element('entry')
        m2.set("xml:lang","en")
        root.append (m2)
        reverted_count=str(blogobj.reverted_count)
        if reverted_count == "None" :
            uid = "urn:publicid:ap.shakticoin:"+str(blogobj.unique_id)+"0"
        else:
            uid = "urn:publicid:ap.shakticoin:"+str(blogobj.unique_id)+reverted_count

        

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:]
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:]
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)
        images_obj = moreimages_apwire.objects.filter(post = blogobj)
        a = et.SubElement(m2,"category")
        a.set("label","Global")
        a.set("term","Global")
        a.set("scheme","http://cv.ap.org/keyword")
        b1 = et.SubElement(m2, "link")
        
        if reverted_count == "None" :
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"0")
        else:
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)
        b1.set("rel","related")
        topic_replacedwithunderscore = str(blogobj.topic).replace(" ","_")
        b1 = et.SubElement(m2, "link")
        b1.set("rel","alternate")
        b1.set('href','https://shakticoin.com/en/blog/{}'.format(topic_replacedwithunderscore))

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
        elee = et.SubElement(m2,"apcm:ContentMetadata")
        elem = et.SubElement(elee,"apcm:HeadLine")
        elem.text=str(blogobj.topic)
        elem = et.SubElement(elee,"apcm:Characteristics")
        elem.set("MediaType","Text")
        elem = et.SubElement(elee,'link')
        elem.set('href','https://ap.shakticoin.com/viewxml/{}'.format(blogobj.pk))
        elem.set("rel","self")

        elee = et.SubElement(m2,"apnm:NewsManagement")
        elem = et.SubElement(elee,"apnm:ManagementId")
        if reverted_count == "None" :
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"0"
        else:
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"
    
        x = blogobj.description.split("\n")
        print(x)
        y = []
        z=[]
        count = 0
        for i in x:
            count += 1
            if count % 2 != 0:
                y.append(i)
        for i in y:  
            i = i.replace("&nbsp;","")
            i = i.replace("&#39;","")
            z.append(i)
            soup = bs(i,'html.parser')
            results = soup.find_all('a')
            print(results)
            i = re.sub('<[^<]*?/?>', ' ', i)
            ele = et.SubElement(o1, "apxh:p")
            ele.text = str(i)
            for obj in results:
                ele1 = et.SubElement(ele,"apxh:a")
                ele1.set("href",str(obj['href']))
                # ele1.set("target","_blank")
                ele1.set("rel","nofollow noopener")
                ele1.text=str(obj.text)
        

        m2 = et.Element('entry')
        m2.set("xml:lang","en")
        root.append (m2)

        if reverted_count == "None" :
            uid = "urn:publicid:ap.shakticoin.com:"+randno+"0"
        else:
            uid = "urn:publicid:ap.shakticoin.com:"+randno+reverted_count

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:]
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:]
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        

        if blogobj.image :
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 

        if images_obj:
            for i in images_obj:
                a5 = et.SubElement(m2,'content')
                a5.set("type","image/jpeg")
                a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(i.image)) 
        
        # b1 = et.SubElement(m2, "link")
        # b1.set("rel","related")
        # if reverted_count == "None" :
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"0")
        # else:
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)

        elee = et.SubElement(m2,"apcm:ContentMetadata")
        elem = et.SubElement(elee,"apcm:HeadLine")
        elem.text=str(blogobj.topic)
        elem = et.SubElement(elee,"apcm:Characteristics")
        elem.set("MediaType","Photo")

        elee = et.SubElement(m2,"apnm:NewsManagement")
        elem = et.SubElement(elee,"apnm:ManagementId")
        if reverted_count == "None" :
            elem.text = "urn:publicid:ap.shakticoin.com:"+randno+"0"
        else:
            elem.text = "urn:publicid:shakticoin:"+randno+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"
        

        

    
      
    tree = et.ElementTree(root)
    xmlfolder_exist()
    tree.write('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), encoding="utf-8",xml_declaration=True)

class xmlValue:

    def __init__(self,file):
        self.data = str(file)
        self.status_code = 200

    def get(self,file):
        return self.__str__
    
    def __str__(self) -> str:
        return self.data
 #////////////
def viewxmlall(request):
    buildxmlall()
    response = open(f"{MEDIA_ROOT}/xml/output_xml_Blog_AP_Wire.xml", 'rb')
    return HttpResponse(response.read(),content_type="application/xml")


#////////////
def buildxmlall2():
    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","https://www.w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://ap.org/schemas/03/2005/apcm")
    root.set("xml:lang","en")
    print("here")
    

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "ShaktiCoin"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://shakticoin.com/"
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    # para = ET.SubElement(..., "p", link_id=1)
    # ET.SubElement(para, "link", id=2, type="external", url="http://www.google.com").text="Google.com"

    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"

    # current time and timezone
    now = str(datetime.now())
    now_format = now
    now_format = now[:10]+"T"+now[11:]

    from django.utils.timezone import get_current_timezone
    current_tz = get_current_timezone()


    if str(current_tz) == "UTC":
        tz_format = "00:00"

    a7 = et.SubElement(root,'updated')
    a7.text = now_format+"+"+tz_format

    

    blogall = Ap_News.objects.filter(Q(status="Ready_For_Release") | Q(status="App_Published"))
    for blogobj in blogall:        
        randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        m2 = et.Element('entry')
        m2.set("xml:lang","en")
        root.append (m2)
        reverted_count=str(blogobj.reverted_count)
        if reverted_count == "None" :
            uid = "urn:publicid:ap.shakticoin:"+str(blogobj.unique_id)+"0"
        else:
            uid = "urn:publicid:ap.shakticoin:"+str(blogobj.unique_id)+reverted_count

        

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:]
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:]
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)
        images_obj = moreimages_apnews.objects.filter(post = blogobj)
        a = et.SubElement(m2,"category")
        a.set("label","Global")
        a.set("term","Global")
        a.set("scheme","http://cv.ap.org/keyword")
        b1 = et.SubElement(m2, "link")
        
        if reverted_count == "None" :
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"0")
        else:
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)
        b1.set("rel","related")
        topic_replacedwithunderscore = str(blogobj.topic).replace(" ","_")
        b1 = et.SubElement(m2, "link")
        b1.set("rel","alternate")
        b1.set('href','https://shakticoin.com/en/blog/{}'.format(topic_replacedwithunderscore))

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
        elee = et.SubElement(m2,"apcm:ContentMetadata")
        elem = et.SubElement(elee,"apcm:HeadLine")
        elem.text=str(blogobj.topic)
        elem = et.SubElement(elee,"apcm:Characteristics")
        elem.set("MediaType","Text")
        elem = et.SubElement(elee,'link')
        elem.set('href','https://ap.shakticoin.com/viewxml/{}'.format(blogobj.pk))
        elem.set("rel","self")

        elee = et.SubElement(m2,"apnm:NewsManagement")
        elem = et.SubElement(elee,"apnm:ManagementId")
        if reverted_count == "None" :
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"0"
        else:
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"
    
        x = blogobj.description.split("\n")
        print(x)
        y = []
        z=[]
        count = 0
        for i in x:
            count += 1
            if count % 2 != 0:
                y.append(i)
        for i in y:  
            i = i.replace("&nbsp;","")
            i = i.replace("&#39;","")
            z.append(i)
            soup = bs(i,'html.parser')
            results = soup.find_all('a')
            print(results)
            i = re.sub('<[^<]*?/?>', ' ', i)
            ele = et.SubElement(o1, "apxh:p")
            ele.text = str(i)
            for obj in results:
                ele1 = et.SubElement(ele,"apxh:a")
                ele1.set("href",str(obj['href']))
                # ele1.set("target","_blank")
                ele1.set("rel","nofollow noopener")
                ele1.text=str(obj.text)
        

        m2 = et.Element('entry')
        m2.set("xml:lang","en")
        root.append (m2)

        if reverted_count == "None" :
            uid = "urn:publicid:ap.shakticoin.com:"+randno+"0"
        else:
            uid = "urn:publicid:ap.shakticoin.com:"+randno+reverted_count

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:]
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:]
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        

        if blogobj.image :
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(blogobj.image)) 

        if images_obj:
            for i in images_obj:
                a5 = et.SubElement(m2,'content')
                a5.set("type","image/jpeg")
                a5.set("src","https://shaktidjangoblog-prod.s3.amazonaws.com/"+str(i.image)) 
        
        # b1 = et.SubElement(m2, "link")
        # b1.set("rel","related")
        # if reverted_count == "None" :
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"0")
        # else:
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+reverted_count)

        elee = et.SubElement(m2,"apcm:ContentMetadata")
        elem = et.SubElement(elee,"apcm:HeadLine")
        elem.text=str(blogobj.topic)
        elem = et.SubElement(elee,"apcm:Characteristics")
        elem.set("MediaType","Photo")

        elee = et.SubElement(m2,"apnm:NewsManagement")
        elem = et.SubElement(elee,"apnm:ManagementId")
        if reverted_count == "None" :
            elem.text = "urn:publicid:ap.shakticoin.com:"+randno+"0"
        else:
            elem.text = "urn:publicid:shakticoin:"+randno+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"
        

        

    
      
    tree = et.ElementTree(root)
    xmlfolder_exist()
    tree.write('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), encoding="utf-8")
    


def viewxmlall2(request):
    buildxmlall2()
    print("call")
    response = FileResponse(open(f"{MEDIA_ROOT}/xml/output_xml_Blog_AP_News.xml", 'rb')) 
    return response



def downloadxmlall(request):
    
    buildxmlall()
    
    # Pathout is the path to the output.xml
    xmlFile = open('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), 'r')
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')

    response['Content-Disposition'] = "attachment; filename=output_xml_Blogs_AP_Wire.xml"
    return response





def downloadxmlall2file2(request):
    
    buildxmlall2()
    # Pathout is the path to the output.xml
    

    xmlFile = open('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')

    response['Content-Disposition'] = "attachment; filename=output_xml_Blogs_AP_Wire.xml"
    return response

def createBlog(request):
    print("Createblog")
    if request.method == 'POST':
        cat = request.POST['category']
        if cat == "Select Category":
            cat_obj = None
        else:
            cat_obj= category.objects.get(id=cat)

        sel = request.POST['status']
        


        blog = Ap_Wire.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description'],status="Content_Pitching",category=cat_obj,blog_release_status=sel)
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()
        
        
        if 'extra_imagewire[]' in request.FILES:
            files = request.FILES.getlist('extra_imagewire[]')
            for i in files:                
                moreimages_apwire.objects.create(post=blog,image=i)

        print("---------------")
        print(sel)

        return redirect('viewfunction')

    return render(request,'createBlog.html')

def createBlog2(request):
    print("Createblog2")
    if request.method == 'POST':
        cat = request.POST['category']
        if cat == "Select Category":
            cat_obj = None
        else:
            cat_obj= category.objects.get(id=cat)

        sel = request.POST['status']
        
        

        blog = Ap_News.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description2'],status="Content_Pitching",category=cat_obj,blog_release_status=sel)
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()

        if 'extra_imagenews[]' in request.FILES:
            files = request.FILES.getlist('extra_imagenews[]')
            for i in files:                
                moreimages_apnews.objects.create(post=blog,image=i)
            
        return redirect('/?secondTab=True')

    return render(request,'createBlog.html')



@csrf_exempt
def dropData(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)
        
        
        blog = Ap_Wire.objects.get(pk=dropid)
        blog.status= addedto
        blog.save()
        desc = blog.description
        desc = desc.replace("&nbsp;","")
        desc = desc.replace("&#39;","")
        desc = re.sub('<[^<]*?/?>', '', desc)
        splitdesc = desc.split()
        description_count = len(splitdesc)-2
        roles = [
            'Content_Pitching',
            'Writing_Rewrite',
            'Review_Draft_1',
            'Review_Draft_2',
            'FDN_Approval_1',
            'Ready_For_Release',
            'App_Published'
        ]
        key_list = list(roles)
        index = key_list.index(addedto)
        print(removedfrom)
        if removedfrom == "App_Published":
            
            blog.reverted_count += 1
            blog.save()
        if permissions.objects.filter(user__in = [request.user],status=addedto).exists():
            permiss = permissions.objects.filter(user = request.user,status=addedto).first()
            
            
            access_dict = {
                'create':permiss.create ,
                'edit':permiss.edit ,
                'view':permiss.view ,
                'to_delete':permiss.to_delete ,
                'move':permiss.move,
                'publish':permiss.publish
            }



        return JsonResponse({'msg':'success','access_dict':access_dict,'tableIndex':index+1,'description_count':description_count})


@csrf_exempt
def dropData2(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)

        blog = Ap_News.objects.get(pk=dropid)
        blog.status= addedto
        blog.save()

        desc = blog.description
        desc = desc.replace("&nbsp;","")
        desc = desc.replace("&#39;","")
        desc = re.sub('<[^<]*?/?>', '', desc)
        splitdesc = desc.split()
        description_count = len(splitdesc)-2
        roles = [
            'Content_Pitching',
            'Writing_Rewrite',
            'Review_Draft_1',
            'Review_Draft_2',
            'FDN_Approval_1',
            'Ready_For_Release',
            'App_Published'
        ]
        key_list = list(roles)
        index = key_list.index(addedto)
        if removedfrom == "App_Published":
            blog.reverted_count += 1
            blog.save()
        if permissions.objects.filter(user__in = [request.user],status=addedto).exists():
            permiss = permissions.objects.filter(user = request.user,status=addedto).first()
            
            
            access_dict = {
                'create':permiss.create ,
                'edit':permiss.edit ,
                'view':permiss.view ,
                'to_delete':permiss.to_delete ,
                'move':permiss.move,
                'publish':permiss.publish
            }
        return JsonResponse({'msg':'success','access_dict':access_dict,'tableIndex':index+1,'description_count':description_count})

def deleteBlog(request,pk):
    blogobj = Ap_Wire.objects.filter(pk=pk)
    name=Ap_Wire.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('viewfunction')

def deleteBlog2(request,pk):
    blogobj = Ap_News.objects.filter(pk=pk)
    name=Ap_News.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('/?secondTab=True')

def logout_view(request):
    logout(request)
    return redirect('loginview')

def addimagewire(req,pk):
    if request.method == 'POST':

        blogobj = Ap_Wire.objects.get(pk=pk)

        if 'image' in request.FILES:
            image=request.POST['image']
            moreimages_apwire.objects.create(post = blogobj,image=image)
        
        return redirect('viewfunction')

    return redirect('viewfunction')


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

#image

def imageview(request):
    ap_wire_img = Ap_Wire.objects.all()
    ap_news_img = Ap_News.objects.all()
    extra_img = Mangeimages.objects.all()
    return render(request,'images.html',{"img":ap_wire_img,"img2":ap_news_img,"extra_img":extra_img})

def uploadimage(request):
    if request.method == "POST":
        image=request.FILES['Mangeimages']
        mangeimages = Mangeimages(image=image)
        mangeimages.save()
    return redirect('imageview')