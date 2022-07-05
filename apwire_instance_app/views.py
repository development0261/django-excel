from django.shortcuts import render
from app.models import Ap_Wire,Ap_News,content_brief,permissions,category,Mangeimages
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import redirect
# Create your views here.

# ////////////////////// HOMEVIEW ////////////////////////////////////////

def apwire_published(request):
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
        

        apwire_APPublished_data = Ap_Wire.objects.filter(status='App_Published')
        context_dict = {}   
        context_dict['App Published'] = apwire_APPublished_data



        
        

        

        obj = content_brief.objects.all()
        if obj:
            context = obj
        else:
            context = None
    
        permissions.objects.filter(user=request.user)

        categories = category.objects.all()

        new_images_dict = Mangeimages.objects.all()


        

        users = User.objects.values()
        return render(request,'apwire_instance.html',{'user_dict':users,'context_dict':context_dict,'category_dict':categories,'context':context,'new_images_dict':new_images_dict})
        
    else:        
        return redirect('login_instance')


# ////////////////////// AUTHENTICATION ////////////////////////////////////////

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def login_instance(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)
        if not User.objects.filter(username=username).exists():
            messages.warning(request, f'User with username "{username}" does not exist') 
            return redirect('apwire_instance')
        elif User.objects.filter(username=username).exists():
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('apwire_instance')

                else:
                    messages.error(request, 'user is inactive') 
                    return redirect('apwire_instance')

            else:
                messages.warning(request, 'Incorrect Password') 
                return redirect('apwire_instance')
        else:
            return redirect('apwire_instance')

    else:
        return render(request,'login_instnace.html')



def register_instance(request):
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
                return redirect('apwire_instance')
            else:
                messages.warning(request,"Passwords don't match")
                return redirect('register_instance')
        if User.objects.filter(username=username).exists():
            messages.warning(request,"This user already exists")
            return redirect('register_instance')
    else:
        return render(request,'register_instance.html',{'registered':registered})

def logout_instance(request):
    logout(request)
    return redirect('login_instance')