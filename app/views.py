from ast import While
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

def newline():
    pass

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
        print(request.POST['description'])
        blog = Blog.objects.filter(pk=pk).update(topic=request.POST['topic'],author=request.user,description=request.POST['description'])
       
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
    topic = request.POST['topic']
    description = request.POST['description']
    print(topic)
    print(description)
 
    
    tableObj = Blog.objects.get(pk = id)
    
    print(id)
    
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




def publishBlog2(request,pk):
    blogobj = Blog2.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.publishedon = datetime.today().date()
    blogobj.save()

    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))

    filepath = downloadxml(request,pk,stringPath=True)
    return redirect('/?filepath={}'.format(filepath))

def printpdf(desc,imagepath,topic):
    import time
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    topic=str(topic)
    doc = SimpleDocTemplate(f"{topic}.pdf",pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    Story=[]

    im = Image(imagepath, 6*inch, 4*inch)
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
    doc.build(Story)
    response = FileResponse(open(f"{topic}.pdf", 'rb'),as_attachment=True)
    return response


def downloadpdf(request,pk):
    blogobj = Blog.objects.get(pk=pk)
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

    pdf = printpdf(z,image_data,str(blogobj.topic)) 
    return pdf

def downloadpdf2(request,pk):
    blogobj = Blog2.objects.get(pk=pk)
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

    pdf = printpdf(z,image_data,str(blogobj.topic))
    return pdf



def downloadxml(request,pk,stringPath= None):
    blogobj = Blog.objects.get(pk=pk)
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
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    a5 = et.SubElement(root,'link')
    a5.set("href","https://draftblog.shakticoin.com/post-sitemap.xml")
    a5.set("rel","self")
    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-19T01:58:31Z"

    m2 = et.Element('entry')
    m2.set("xml:lang","en-us")
    root.append (m2)

    
    uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    b5.text = str(blogobj.publishedon)
    b6 = et.SubElement(m2, "updated")
    b6.text = str(blogobj.updated)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)

    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
    
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
        # for x in listtext:
        #     ele1 = et.SubElement(ele,"apxh:a")
        
    # print(z)
        

        
        
        # soup = bs(str(i))
        # soup.findAll(href='https://stackoverflow.com/')

        # import re
        # m = re.search('(<a .*>)', i)
        # if m:
        #     print("flag hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #     print(m.group(1))
        # ele = et.SubElement(o1, "apxh:p")
        # ele.text = str(i)
    
    

    
    
    tree = et.ElementTree(root)

    tree2 = et.ElementTree(root)
    
  

    tree.write('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8")
    
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
    blogobj = Blog.objects.get(pk=pk)
    blogobj.status = "App_Published"
    blogobj.publishedon = datetime.today().date()
    blogobj.save()
    
    messages.success(request,"Your blog {} for AP Wire is Published".format(blogobj.topic))

    filepath = downloadxml(request,pk,stringPath=True)
    return redirect('/?filepath={}'.format(filepath))

def downloadxmlfile2(request,pk):
    blogobj = Blog.objects.get(pk=pk)
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

    
    uid = "urn:publicid:www.heart.org:"+str(blogobj.unique_id)+"-2"

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    b5.text = str(blogobj.publishedon)
    b6 = et.SubElement(m2, "updated")
    b6.text = str(blogobj.updated)
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



    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
 
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
        
        i = i.replace("<p>","")
        i = i.replace("</p>","")
        i = i.replace("<em>","")
        i = i.replace("</em>","")
        i = i.replace("<strong>","")
        i = i.replace("</strong>","")   
        i = i.replace("&nbsp;","")
        z.append(i)
        
        ele = et.SubElement(o1, "apxh:p")
        ele.text = str(i)
    
    

    
    
    tree = et.ElementTree(root)

    tree2 = et.ElementTree(root)
    

  

    tree.write('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), encoding="utf-8")
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_Wire_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')
    response['Content-Disposition'] = "attachment; filename=output_xml_Blog_AP_Wire_{}_{}.xml".format(blogobj.pk,blogobj.topic)

    return response

def downloadxml2(request,pk,stringPath= None):
    blogobj = Blog2.objects.get(pk=pk)

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
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    

    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-19T01:58:31Z"

    m2 = et.Element('entry')
    m2.set("xml:lang","en-us")
    root.append (m2)

    
    uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    b5.text = str(blogobj.publishedon)
    b6 = et.SubElement(m2, "updated")
    b6.text = str(blogobj.updated)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)

    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
 
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
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')
    response['Content-Disposition'] = "attachment; filename=output_xml_Blog_AP_Wire_{}_{}.xml".format(blogobj.pk,blogobj.topic)
    
    if stringPath:
        return '/media/xml/output_xml_Blog_AP_Wire_{}.xml'.format(blogobj.pk)
    else:
        return response

def downloadxml2file2(request,pk):
    blogobj = Blog2.objects.get(pk=pk)

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

    
    uid = "urn:publicid:www.heart.org:"+str(blogobj.unique_id)+"-2"

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    b5.text = str(blogobj.publishedon)
    b6 = et.SubElement(m2, "updated")
    b6.text = str(blogobj.updated)
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

    
    uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

    b1 = et.SubElement(m2, "id")
    b1.text = str(uid)
    b5 = et.SubElement(m2, "published")
    b5.text = str(blogobj.publishedon)
    b6 = et.SubElement(m2, "updated")
    b6.text = str(blogobj.updated)
    b2 = et.SubElement(m2, "title")
    b2.text = str(blogobj.topic)

    n1 = et.Element('content')
    n1.set("type","xhtml")
    m2.append (n1)

    o1 = et.Element('apxh:div')
    n1.append (o1)
 
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
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_News_{}.xml'.format(MEDIA_ROOT,blogobj.pk), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')
    response['Content-Disposition'] = "attachment; filename=output_xml_Blog_AP_Wire_{}_{}.xml".format(blogobj.pk,blogobj.topic)
    
    
    return response


def downloadxmlall(request):
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

    blogall = Blog.objects.filter(status="Ready_For_Release")
    for blogobj in blogall:
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        b5.text = str(blogobj.publishedon)
        b6 = et.SubElement(m2, "updated")
        b6.text = str(blogobj.updated)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
    
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
        print(z)

    
      
    tree = et.ElementTree(root)




    tree.write('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), encoding="utf-8")
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')

    response['Content-Disposition'] = "attachment; filename=output_xml_Blogs_AP_Wire.xml"
    return response


def downloadxmlallfile2(request):
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

    blogall = Blog.objects.filter(status="App_Published")
    for blogobj in blogall:
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        b5.text = str(blogobj.publishedon)
        b6 = et.SubElement(m2, "updated")
        b6.text = str(blogobj.updated)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
    
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
        print(z)

    
      
    tree = et.ElementTree(root)




    tree.write('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), encoding="utf-8")
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_Wire.xml'.format(MEDIA_ROOT), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')

    response['Content-Disposition'] = "attachment; filename=output_xml_Blogs_AP_Wire.xml"
    return response


def downloadxmlall2(request):
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
    a3 = et.SubElement(root,"id")
    a3.text = "shakticoin123"
    a4 = et.SubElement(root,"title")
    a4.text = "ShaktiCoin"
    

    a6 = et.SubElement(root,'rights')
    a6.text = "Copyright 2022 ShaktiCoin"
    a7 = et.SubElement(root,'updated')
    a7.text = "2022-03-19T01:58:31Z"

    m2 = et.Element('entry')
    root.append (m2)

    


    blogall = Blog2.objects.filter(status="Ready_For_Release")
    for blogobj in blogall:
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        b5.text = str(blogobj.publishedon)
        b6 = et.SubElement(m2, "updated")
        b6.text = str(blogobj.updated)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
    
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
            print(i)
            i = i.replace("<p>","")
            i = i.replace("</p>","")
            i = i.replace("<em>","")
            i = i.replace("</em>","")
            i = i.replace("<strong>","")
            i = i.replace("</strong>","")   
            i = i.replace("&nbsp;","")
            z.append(i)
            ele = et.SubElement(o1, "apxh:p")
            ele.text = str(i)
        print(z)

    
      
    tree = et.ElementTree(root)
      
    



    tree.write('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), encoding="utf-8")
    
    # Pathout is the path to the output.xml
    
    xmlFile = open('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), 'r')
    print(xmlFile)
    myfile = xmlFile.read()
    response = HttpResponse(myfile, content_type='application/xml')

    response['Content-Disposition'] = "attachment; filename=output_xml_Blogs_AP_Wire.xml"
    return response

def downloadxmlall2file2(request):
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
    


   

    


    blogall = Blog2.objects.filter(status="Ready_For_Release")
    for blogobj in blogall:
        m2 = et.Element('entry')
        m2.set("xml:lang","en-us")
        root.append (m2)
        uid = "urn:publicid:shakticoin:"+str(blogobj.unique_id)+"-2"

        b1 = et.SubElement(m2, "id")
        b1.text = str(uid)
        b5 = et.SubElement(m2, "published")
        b5.text = str(blogobj.publishedon)
        b6 = et.SubElement(m2, "updated")
        b6.text = str(blogobj.updated)
        b2 = et.SubElement(m2, "title")
        b2.text = str(blogobj.topic)

        n1 = et.Element('content')
        n1.set("type","xhtml")
        m2.append (n1)

        o1 = et.Element('apxh:div')
        n1.append (o1)
    
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
        print(z)

    
      
    tree = et.ElementTree(root)
      
    



    tree.write('{}/xml/output_xml_Blog_AP_News.xml'.format(MEDIA_ROOT), encoding="utf-8")
    
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
        return redirect('/?secondTab=True')

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

def deleteBlog(request,pk):
    blogobj = Blog.objects.filter(pk=pk)
    name=Blog.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('view')

def deleteBlog2(request,pk):
    blogobj = Blog2.objects.filter(pk=pk)
    name=Blog2.objects.get(pk=pk).topic
    blogobj.delete()
    messages.info(request,"Blog {} has been deleted".format(name))
    return redirect('view')

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