from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import authenticate
from .models import *


# Create your views here.

def admin(request):
    if 'user' in request.session:
        return redirect('admin_index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:

            if user.is_superuser:

                request.session['user']=username
            
                return redirect('admin_index')
        else:

            return render(request,'admin_login.html')

    return render(request,'admin_login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_index(request):

    if 'user' in request.session:
        objs = User.objects.all()
        return render(request,'admin_index.html',{'objs': objs})
    else:
        print('dsvsdvsvf-----------------')
        
    return render(request,'admin_login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    if 'user' in request.session:
         del request.session['user']
    
    return redirect('admin')

# ............Category..........


@login_required(login_url='/admin')
def category_management(request):

   #context =  { 'category':Category.objects.all()}

     
  
   return render(request,'category_management.html',context)    

@login_required(login_url='/admin')
def add_category(request):
    if request.method == 'POST':
        
       # category_name = request.POST['category_name']
       # cata= Category.objects.filter(category_name= category_name)
        if cata.exists():
            
     
        
            messages.success(request, 'Category already exists')
            return redirect('add_category')
        else:
            #category = Category.objects.Create(category_name=category_name)
            category.save()
            return render(request, 'category_managment.html')
    return render(request, 'add_category.html')




#usermngmt----------------
def user_view(request):
    users=User.objects.all()
    context={'users':users}
    return render(request,"users.html",context)

def block_user(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    print('user blocked')
    return redirect('user_view')




def unblock_user(request,id):
    user = User.objects.get(id= id)
    user.is_active  = True
    user.save()
    print('user is active')
    return redirect('user_view')
 
def delete(request,id):
    my= User.objects.get(id=id)
    my.delete()
    return redirect('user_view')
    
