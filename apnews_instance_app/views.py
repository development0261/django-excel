from django.shortcuts import render
from app.models import Ap_News,content_brief,permissions,category,Mangeimages
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import redirect
# ///////////////////////////////// HOME VIEW ///////////////////////////////////
        
def apnews_published(request):

    if request.user.is_authenticated:
        

        apnews_APPublished_data = Ap_News.objects.filter(status='App_Published')
        context_dict = {}   
        context_dict['App Published'] = apnews_APPublished_data

        obj = content_brief.objects.all()
        if obj:
            context = obj
        else:
            context = None
    
        permissions.objects.filter(user=request.user)

        categories = category.objects.all()

        new_images_dict = Mangeimages.objects.all()

        users = User.objects.values()
        return render(request,'apnews_instance.html',{'user_dict':users,'context_dict':context_dict,'category_dict':categories,'context':context,'new_images_dict':new_images_dict})
        
    else:        
        return redirect('login_instance')

