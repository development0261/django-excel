import random,string    
from itertools import count
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
                return redirect('view')
            else:
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
    
    tableObj = Ap_Wire.objects.get(pk = id)
    date = tableObj.date
    formatedDate = date.strftime('%Y-%m-%d')
    # image = tableObj.image
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
    imageobjs = moreimages_apwire.objects.filter(post = tableObj)
    if not imageobjs:
        imgdict = {}
    else:
        imgdict = {}
        count = 0
        for i in imageobjs:
            count += 1
            imgdict[str(count)]=i.image.url
        
    return JsonResponse({'category':tableObj.category.name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj,'imgdict':imgdict})

def contentgetRowData(request):
    pass

def getRowData2(request,id,tableName):
    
    tableObj = Ap_News.objects.get(pk = id)
    date = tableObj.date
    formatedDate = date.strftime('%Y-%m-%d')
    imageobj = None
    if tableObj.image:
        imageobj =tableObj.image.url
        imageobjs = moreimages_apnews.objects.filter(post = tableObj)
    if not imageobjs:
        imgdict = {}
    else:
        imgdict = {}
        count = 0
        for i in imageobjs:
            count += 1
            imgdict[str(count)]=i.image.url
        
    return JsonResponse({'category':tableObj.category.name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk,'content':tableObj.description,'image':imageobj,'imgdict':imgdict})

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
        
        

        return redirect('view')
    return render(request,'editblog.html')  

@csrf_exempt
def editData(request,id,tableName):
    print(request.POST)
    topic = request.POST['topic']
    description = request.POST['description']
    cat_id = request.POST['category']
    tableObj = Ap_Wire.objects.get(pk = id)
    
    cat_obj = category.objects.get(id=cat_id)
    
    tableObj.description = description
    tableObj.topic = topic
    tableObj.category = cat_obj
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

    formatedDate = date.strftime('%B %d,%Y')
    return JsonResponse({'category':tableObj.category.name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk})

@csrf_exempt
def editData2(request,id,tableName):
    topic = request.POST['topic']
    description = request.POST['description']
    cat_id = request.POST['category']
    
    cat_obj = category.objects.get(id=cat_id)
    
    tableObj = Ap_News.objects.get(pk = id)
    tableObj.category = cat_obj
    tableObj.description = description
    tableObj.topic = topic
    tableObj.save()
    if 'image' in request.FILES:
        image=request.FILES['image']
        tableObj.image = image
        tableObj.save()

    count = 0
    if f'image{count}' in request.FILES:    
        moreimages_apnews.objects.filter(post=tableObj).delete()
        for i in request.FILES:
            moreimages_apnews.objects.create(post=tableObj,image=request.FILES[f'image{count}'])
            count += 1
        

    date = datetime.strptime(str(tableObj.date), '%Y-%m-%d')

    formatedDate = date.strftime('%B %d,%Y')
    return JsonResponse({'category':tableObj.category.name,'topic':tableObj.topic,'author':tableObj.author.username,'date':formatedDate,'pk':tableObj.pk})



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

        obj = content_brief.objects.first()
        if obj:
            topic = obj.topic
            desc = obj.description
        else:
            topic = None
            desc = None
        
        # desc = desc.replace("&nbsp;","")
        # desc = desc.replace("&#39;","")
        # desc = re.sub('<[^<]*?/?>', ' ', desc)

        print(desc)




        permissions.objects.filter(user=request.user)

        categories = category.objects.all()


        return render(request,'index.html',{'context_dict':context_dict,'context_dict1':context_dict1,'category_dict':categories,'topic':topic,'description':desc})
    else:
        return redirect('loginview')






def publishBlog2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.published_on = datetime.today().date()
    blogobj.save()

    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))

    filepath = downloadxml(request,pk,stringPath=True)
    return redirect('/?filepath={}'.format(filepath))

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
                            topMargin=72,bottomMargin=18)
    Story=[]
    im = Image(imagepath, 6*inch, 3.5*inch)
    Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = topic
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
    x=doc.build(Story)
    response = FileResponse(open(f"{MEDIA_ROOT}/pdf/{topic}.pdf", 'rb'),as_attachment=True)
    return response

def buildxml(pk,blogobj):
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
    a2.text = "https://ap.shakticoin.com//"
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
    a7.text = str(blogobj.updated)


    m2 = et.Element('entry')
    m2.set("xml:lang","en-us")
    root.append (m2)

    reverted_count=str(blogobj.reverted_count)
    if reverted_count == "None" :
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
    else:
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:19]+"Z"
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:25]+"Z"
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)
    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://ap.shakticoin.com/media/"+str(blogobj.image)) 
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
        elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
    else:
        elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count
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
            ele1.set("target","_blank")
            ele1.set("rel","nofollow noopener")
            ele1.text=str(obj.text)

    tree = et.ElementTree(root)

    tree2 = et.ElementTree(root)

    tree.write('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8")

    # response = FileResponse(open(f"{MEDIA_ROOT}/xml/{topic}.pdf", 'rb'),as_attachment=True)

    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","http://w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://www.w3.org/2005/Atom")
    root.set("xml:lang","en-us")

    q1 = et.SubElement(root,"title")
    q1.text = "American Heart Association News"

    m1 = et.Element('link')
    m1.set("rel","self")
    m1.set("href","https://www.heart.org/-/media/RSS-Feeds/apfeed.xml")
    root.append (m1)

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "American Heart Association News"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://www.heart.org"
    a4 = et.SubElement(root,"title")
    a4.text = "American Heart Association News"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-25T14:02:18.6328006Z"
    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 American Heart Association News"
    


    m2 = et.Element('entry')
    m2.set("xml:lang","en-us")
    root.append (m2)

    
    reverted_count=str(blogobj.reverted_count)
    if reverted_count == "None" :
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
    else:
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:19]+"Z"
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:25]+"Z"
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)
    b3 = et.SubElement(m2,'rights')
    b3.text = "Copyright 2022 American Heart Association News"
    a5 = et.SubElement(m2,'link')
    a5.set("rel","alternate")
    a5.set("href","https://www.heart.org/en/news/2022/03/25/5-barriers-to-eating-a-heart-healthy-diet-that-have-nothing-to-do-with-willpower")
    a10 = et.SubElement(m2,'category')
    a10.set("label","English - All US orgs")
    a10.set("term","English - All US orgs")
    a10.set("scheme","http://cv.ap.org/keyword")

    a11 = et.SubElement(m2,'link')
    a11.set("rel","alternate")
    a11.set("href","urn:publicid:www.heart.org:2B6EF1D3FB2C4D8A8D158233FE8C5AD6-2")

    m2 = et.Element('entry')
    m2.set("xml:lang","en-us")
    root.append (m2)

    
    reverted_count=str(blogobj.reverted_count)
    if reverted_count == "None" :
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
    else:
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    updated = str(blogobj.published_on)
    utz = updated[:10]+"T"+updated[11:19]+"Z"
    b5.text = str(utz)
    b6 = et.SubElement(m2, "updated")
    updated = str(blogobj.updated)
    utz = updated[:10]+"T"+updated[11:25]+"Z"
    b6.text = str(utz)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)
    if blogobj.image :
        a5 = et.SubElement(m2,'content')
        a5.set("type","image/jpeg")
        a5.set("src","https://ap.shakticoin.com/media/"+str(blogobj.image)) 
    
    
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
            ele1.set("href",str(obj['href']))
            ele1.set("target","_blank")
            ele1.set("rel","nofollow noopener")
            ele1.text=str(obj.text)
    print(z)
    


    tree = et.ElementTree(root)
    

    tree.write('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8")



def downloadpdf(request,pk):
    blogobj = Ap_Wire.objects.get(pk=pk)
    imglist = []
    
    for i in moreimages_apwire.objects.filter(post=blogobj):
        imglist.append(MEDIA_ROOT+"/"+i.image.name)
    image_data = MEDIA_ROOT+"/"+blogobj.image.name
    print(image_data)
    
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
        
        i = re.sub('<[^<]*?/?>', ' ', i)
        z.append(i)
        
    pdf = printpdf(z,image_data,str(blogobj.topic),imglist) 
    return pdf

def downloadpdf2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    imglist = []
    
    for i in moreimages_apnews.objects.filter(post=blogobj):
        imglist.append(MEDIA_ROOT+"/"+i.image.name)
    image_data = MEDIA_ROOT+"/"+blogobj.image.name
    print(image_data)
    
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
        
        i = re.sub('<[^<]*?/?>', ' ', i)
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


    return redirect('view')

def backblog2(request,pk):
    blogobj = Ap_News.objects.get(pk=pk)
    blogobj.status = "Content_Pitching"
    blogobj.published_on = datetime.today().date()
    blogobj.save()
    
    messages.success(request,"Your blog {} was reverted back to Content Pitching".format(blogobj.topic))


    return redirect('view')

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
    a2.text = "https://ap.shakticoin.com//"
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    # para = ET.SubElement(..., "p", link_id=1)
    # ET.SubElement(para, "link", id=2, type="external", url="http://www.google.com").text="Google.com"

    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-19T01:58:31Z"

    m2 = et.Element('entry')
    root.append (m2)

    blogall = Ap_Wire.objects.filter(Q(status="Ready_For_Release") | Q(status="App_Published"))
    for blogobj in blogall:        
        randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        reverted_count=str(blogobj.reverted_count)
        if reverted_count == "None" :
            uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
        else:
            uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count

        

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:19]+"Z"
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:25]+"Z"
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)
        images_obj = moreimages_apwire.objects.filter(post = blogobj)
        a = et.SubElement(m2,"category")
        a.set("label","Global")
        a.set("term","Global")
        a.set("scheme","http://cv.ap.org/keyword")
        b1 = et.SubElement(m2, "link")
        b1.set("rel","related")
        if reverted_count == "None" :
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"-0")
        else:
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+reverted_count)

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
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
        else:
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count
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
                ele1.set("target","_blank")
                ele1.set("rel","nofollow noopener")
                ele1.text=str(obj.text)
        

        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)

        if reverted_count == "None" :
            uid = "urn:publicid:shakticoin:"+randno+"-0"
        else:
            uid = "urn:publicid:shakticoin:"+randno+"-"+reverted_count

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:19]+"Z"
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:25]+"Z"
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        

        if blogobj.image :
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://ap.shakticoin.com/media/"+str(blogobj.image)) 

        if images_obj:
            for i in images_obj:
                a5 = et.SubElement(m2,'content')
                a5.set("type","image/jpeg")
                a5.set("src","https://ap.shakticoin.com/media/"+str(i.image)) 
        
        # b1 = et.SubElement(m2, "link")
        # b1.set("rel","related")
        # if reverted_count == "None" :
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"-0")
        # else:
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+reverted_count)

        elee = et.SubElement(m2,"apcm:ContentMetadata")
        elem = et.SubElement(elee,"apcm:HeadLine")
        elem.text=str(blogobj.topic)
        elem = et.SubElement(elee,"apcm:Characteristics")
        elem.set("MediaType","Text")

        elee = et.SubElement(m2,"apnm:NewsManagement")
        elem = et.SubElement(elee,"apnm:ManagementId")
        if reverted_count == "None" :
            elem.text = "urn:publicid:shakticoin:"+randno+"-0"
        else:
            elem.text = "urn:publicid:shakticoin:"+randno+"-"+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"
        

        

    
      
    tree = et.ElementTree(root)
    
    tree.write('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), encoding="utf-8")

def buildxmlall2():
    root = et.Element('feed')
    root.set("xmlns:apnm","http://ap.org/schemas/03/2005/apnm")
    root.set("xmlns:apxh","http://w3.org/1999/xhtml")
    root.set("xmlns:ap","http://ap.org/schemas/03/2005/aptypes")
    root.set("xmlns","http://www.w3.org/2005/Atom")
    root.set("xmlns:apcm","http://www.w3.org/2005/Atom")
    root.set("xml:lang","en-us")

    q1 = et.SubElement(root,"title")
    q1.text = "American Heart Association News"

    m1 = et.Element('link')
    m1.set("rel","self")
    m1.set("href","https://www.heart.org/-/media/RSS-Feeds/apfeed.xml")
    root.append (m1)

    m1 = et.Element('author')
    root.append (m1)
    a1= et.SubElement(m1,"name")
    a1.text = "American Heart Association News"
    a2= et.SubElement(m1,"uri")
    a2.text = "https://www.heart.org"
    a4 = et.SubElement(root,"title")
    a4.text = "American Heart Association News"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-25T14:02:18.6328006Z"
    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 American Heart Association News"
    

    blogall = Ap_News.objects.filter(Q(status="Ready_For_Release") | Q(status="App_Published"))
    for blogobj in blogall:        
        randno = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        reverted_count=str(blogobj.reverted_count)
        if reverted_count == "None" :
            uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
        else:
            uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count

        

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:19]+"Z"
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:25]+"Z"
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)
        
        images_obj = moreimages_apnews.objects.filter(post = blogobj)
        
        a = et.SubElement(m2,"category")
        a.set("label","Global")
        a.set("term","Global")
        a.set("scheme","http://cv.ap.org/keyword")

        b1 = et.SubElement(m2, "link")
        b1.set("rel","related")
        if reverted_count == "None" :
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"-0")
        else:
            b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+reverted_count)

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
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-0"
        else:
            elem.text = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-"+reverted_count
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
                ele1.set("target","_blank")
                ele1.set("rel","nofollow noopener")
                ele1.text=str(obj.text)
        
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        if reverted_count == "None" :
            uid = "urn:publicid:shakticoin:"+randno+"-0"
        else:
            uid = "urn:publicid:shakticoin:"+randno+"-"+reverted_count

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        updated = str(blogobj.published_on)
        utz = updated[:10]+"T"+updated[11:19]+"Z"
        b5.text = str(utz)
        b6 = et.SubElement(m2, "updated")
        updated = str(blogobj.updated)
        utz = updated[:10]+"T"+updated[11:25]+"Z"
        b6.text = str(utz)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)
        

        if blogobj.image :
            a5 = et.SubElement(m2,'content')
            a5.set("type","image/jpeg")
            a5.set("src","https://ap.shakticoin.com/media/"+str(blogobj.image)) 

        if images_obj:
            for i in images_obj:
                a5 = et.SubElement(m2,'content')
                a5.set("type","image/jpeg")
                a5.set("src","https://ap.shakticoin.com/media/"+str(i.image)) 
        
        # b1 = et.SubElement(m2, "link")
        # b1.set("rel","related")
        # if reverted_count == "None" :
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+"-0")
        # else:
        #     b1.set("href","urn:publicid:ap.shakticoin.com:"+randno+"-"+reverted_count)

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
            elem.text = "urn:publicid:shakticoin:"+randno+"-0"
        else:
            elem.text = "urn:publicid:shakticoin:"+randno+"-"+reverted_count
        elem = et.SubElement(elee,"apnm:ManagementType")
        elem.text="Change"
        elem = et.SubElement(elee,"apnm:ManagementSequenceNumber")
        elem.text="3"
        elem = et.SubElement(elee,"apnm:PublishingStatus")
        elem.text="Usable"

    
      
    tree = et.ElementTree(root)
      
    



    tree.write('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), encoding="utf-8")

def viewxmlall(request):
    buildxmlall()
    response = FileResponse(open(f"{MEDIA_ROOT}/xml/output_xml_Blog_AP_Wire.xml", 'rb')) 
    return response


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
        cat_boj = category.objects.get(pk = int(cat))

        blog = Ap_Wire.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description'],status="Content_Pitching",category=cat_boj)
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()
        
        
        if 'extra_image[]' in request.FILES:
            
            files = request.FILES.getlist('extra_image[]')
            for i in files:                
                moreimages_apwire.objects.create(post=blog,image=i)

        return redirect('view')

    return render(request,'createBlog.html')

def createBlog2(request):
    print("Createblog2")
    if request.method == 'POST':
        cat = request.POST['category']
        cat_boj = category.objects.get(pk = int(cat))

        blog = Ap_News.objects.create(topic=request.POST['topic'],author=request.user,description=request.POST['description2'],status="Content_Pitching",category=cat_boj)
        if 'image' in request.FILES:
            image=request.FILES['image']
            blog.image = image
            blog.save()

        if 'extra_image[]' in request.FILES:
            
            files = request.FILES.getlist('extra_image[]')
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
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
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



        return JsonResponse({'msg':'success','access_dict':access_dict,'tableIndex':index+1})


@csrf_exempt
def dropData2(request,dropid,removedfrom,addedto):
    if request.method == "POST":
        print(dropid)
        print(removedfrom)
        print(addedto)

        blog = Ap_News.objects.get(pk=dropid)
        blog.status= addedto
        blog.save()

        blog.save()
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



        return JsonResponse({'msg':'success','access_dict':access_dict,'tableIndex':index+1})

def deleteBlog(request,pk):
    blogobj = Ap_Wire.objects.filter(pk=pk)
    name=Ap_Wire.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('view')

def deleteBlog2(request,pk):
    blogobj = Ap_News.objects.filter(pk=pk)
    name=Ap_News.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('view')

def logout_view(request):
    logout(request)
    return redirect('loginview')

def addimagewire(req,pk):
    if request.method == 'POST':

        blogobj = Ap_Wire.objects.get(pk=pk)

        if 'image' in request.FILES:
            image=request.POST['image']
            moreimages_apwire.objects.create(post = blogobj,image=image)
        
        return redirect('view')

    return redirect('view')


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