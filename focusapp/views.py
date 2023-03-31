from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from user_area.models import users
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate
from django.conf import settings
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import smtplib
import secrets
from admin_app.models import *
from .models import *
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
import random
import razorpay
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers


from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from razorpay.errors import BadRequestError


import os


client = razorpay.Client(auth = (settings.KEY,settings.SECRET))


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index(request):
    pro = products.objects.all()
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"hgfdsdfghgfd_______________________")
    return render(request,'index.html',{'pro': pro})


        

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signup(request):
    global X
    if 'name' in request.session:
        return render (request,'index.html')

    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        userpassword = request.POST.get("password")
        
        print(email)
        print(userpassword)


        if users.objects.filter(email = email).exists(): 
            messages.info(request,"email is already exist")
            return redirect('login')
        elif users.objects.filter(first_name = first_name).exists():
            messages.info(request,"user name exists")
            return redirect('login')
        else:
            
            message = generate_otp()
            sender_email = "itsmekurudan@gmail.com"
            receiver_email = email
            password = "vyuwjybzzhxljzve" 
            settings.X = message
                       
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()

            # request.session['first_name'] = first_name
            # request.session['last_name'] = last_name
            # request.session['email'] = email
            # request.session['password'] = password
            user = users.objects.create_user( first_name = first_name,last_name = last_name, email=email,password=userpassword)
            user.save()
            
            
            
            return redirect('verify_login')

    else:
        return render(request,'signup.html')

def verify_login(request):
    
   
    if request.method =='POST':
        OTP =request.POST['otp']
    
        if OTP == settings.X:
            
            
            return redirect('login')
        else:
            messages.info(request,"invalid otp")       
            return redirect('signup')
    return render(request,'otp_login.html')

def generate_otp(length=6):
    """Generate a one-time password with the specified length."""
    return ''.join(secrets.choice("0123456789") for i in range(length))




        
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)
# class CustomPasswordResetForm(PasswordResetForm):
#     def cleaned_data(self):
#         email = self.cleaned_data.get('email')
#         user_model = users.objects.get(email=email)
#         return {
#             'email': email,
#             'users': user_model,
#         }




# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password_reset.html' # Replace with your template name
#     success_url = reverse_lazy('CustomPasswordResetView') # Replace with your URL name
#     email_template_name = 'password_reset_email.html' # Replace with your email template name
#     form_class = CustomPasswordResetForm
    
#     def as_view(self, **kwargs):
#         # extra_context = {'password': 'password'} # Replace with any additional context variables you want to pass
#         view = super().as_view(extra_context=extra_context, **kwargs)
#         return view
def ForgetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
        print(username,"gjdghjhdj")
        print(email,"huysgdhjdhbjhbnnnnnnnnnnnnnnn")
        if users.objects.filter(first_name=username,email=email).first():
               
                message =generate_otp()
                sender_email = "itsmekurudan@gmail.com"
                receiver_email = email
                subject = "Reset Password OTP"
                passwords = "vyuwjybzzhxljzve" 
                X = message
                request.session['otp'] = X
            
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(sender_email, passwords)
                message = 'Subject: {}\n\n{}'.format(subject, message)
                server.sendmail(sender_email, receiver_email, message)
                server.quit()
                request.session['name'] = username
                
                

                return redirect('password_otp')
                
        else:
             messages.success(request, 'Not user found with this username and email.')
             return redirect('forget_password')
    return render(request,"Forgotpage.html")
def password_otp(request):
    otp = request.session['otp'] 
    
    if request.method =='POST':
       
        OTP =request.POST['otp']
        print(OTP)
    
        if OTP == otp:
           del request.session['otp'] 
           
           
           return redirect('repassword')
        else:
            messages.info(request,"invalid otp") 
    return render(request,'password_verification.html')

def repassword(request):
    if request.method == 'POST':
            newpassword = request.POST.get('new_password')
            repassword = request.POST.get('reconfirm_password')
            
            if  newpassword != repassword:
                   messages.success(request, 'both should  be equal.')
                   return redirect('repassword')
            else:
                usernames= request.session['name']
                del request.session['name']
                print(usernames)
                print('heljfdsodh')
                user_obj=users.objects.get(first_name=usernames)
                user_obj.set_password(newpassword)
                user_obj.save()
                
                messages.success(request, 'password change successfull.')
                return redirect('index')
            

    
    
    
    return render(request,'newpassword.html')



def login(request):
    if 'name' in request.session:
        return render (request,'index.html')
    if request.method == 'POST':  
        email = request.POST['email']
        password = request.POST["password"]
        user = authenticate(email=email,password=password)
        print(user)
        print(email)
        print(password)

        if user is not None:
            request.session['name']=email
            print('index')
          
            
            return redirect('index')

        else:
            messages.info(request,'Enter the correct password')
            print('no pass')
            return redirect('login')

    else:
        return render(request,'login.html')

def logout(request):
     
    request.session.flush()
    print("logout")
    return redirect('index')





def category(request):
    catgry=Category.objects.filter(status=0)
    bran=brands.objects.filter(status=0)
    pro = products.objects.all()

    paginator = Paginator(pro,3)  # 10 items per page

    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
        print(page_data,'try')
    except PageNotAnInteger:
    # If page is not an integer, display the first page.
        page_data = paginator.page(1)
        print(page_data,'except1')
    except EmptyPage:
    # If page is out of range, display the last page of results.
        page_data = paginator.page(paginator.num_pages)
        print(page_data,'except2')

    except Exception as e:
    # Handle any other exceptions that may occur.
        print(f"An error occurred: {e}")
        page_data = paginator.page(1)

    # context={
    #     'cart_items':page_data,
    #     'page_data': page_data,
        
    # }

    context={'catgry':catgry,
    'bran':bran,
    'pro': page_data,
    'page_data': page_data,
        }
    
    return render(request,'category.html',context)

def filter_category(request,id):


    pro = products.objects.filter(category=id)
    print(pro)
    catgry=Category.objects.filter(status=0)
    print(catgry)
    bran=brands.objects.filter(status=0)
    paginator = Paginator(pro,3)  # 10 items per page

    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
        print(page_data,'try')
    except PageNotAnInteger:
    # If page is not an integer, display the first page.
        page_data = paginator.page(1)
        print(page_data,'except1')
    except EmptyPage:
    # If page is out of range, display the last page of results.
        page_data = paginator.page(paginator.num_pages)
        print(page_data,'except2')

    except Exception as e:
    # Handle any other exceptions that may occur.
        print(f"An error occurred: {e}")
        page_data = paginator.page(1)



        

    # context={
    #     'cart_items':page_data,
    #     'page_data': page_data,
        
    # }

    context={'catgry':catgry,
    'bran':bran,
    'pro': page_data,
    'page_data': page_data,
        }
    
    return render(request,'category.html',context)
# def brands(request):
#     bran=brands.objects.filter(status=0)
#     contextt={'bran':bran}
#     return render(request,'category.html',contextt)
def single_product(request,id):
    print(id)
    prdct=products.objects.filter(id=id)

    print(prdct)
    context={
        'prdct':prdct
    }
    return render(request,'single-product.html',context)





# def cart(request):

#     return render(request,'cart.html')
from .models import wishlist

def view_wishlist(request):
    cust = users.objects.get(email=request.session.get('name'))
    wish_items = wishlist.objects.filter(user=cust)
    # wish = wishlist.objects.get(product=product)
    # print(wish,"yyyyyyyyyy")
    total_price = 0
    for item in wish_items:
        ids=item.product.id
        total_price += item.product.price * item.quantity
    return render(request, 'wish_list.html', {'wish_items': wish_items, 'total_price': total_price,'ids':ids})



def add_to_wish(request,id):
  
    product =products.objects.get(id=id)
    print(product,"ttttggvdvbg")
    if product.quantity == 0:
        messages.info(request, 'Product out of stock')
        return redirect('view_wishlist')
    
    else:
        


        cust=users.objects.get(email=request.session.get('name'))
        

        if wishlist.objects.filter(product=product, user=cust):
            wish_item = wishlist.objects.get(product=product)
            wish_item.quantity += 1
            wish_item.save()
            messages.success(request, 'Quantity has been updated')
            return redirect('view_wishlist')
        else:
            wish_item = wishlist(product=product, user=cust, quantity=1)
            wish_item.save()
            messages.success(request, 'Product has been added to your wishlist')
            return redirect('view_wishlist')

def remove_wish(request,id):
    
    pdd = wishlist.objects.get(id=id)
    pdd.delete()
    return redirect('view_wishlist')

def cart(request):
    cust=users.objects.get(email=request.session.get('name'))
    cart_items = Cart.objects.filter(user=cust)

     



    total_price = 0
    pro_total = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
        
        
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price })

def add_to_cart(request,id):
  
    procart = products.objects.get(id=id)
    # product_total=procart.price*procart.quantity
    # print(product_total)
 
    if procart.quantity == 0:
        messages.info(request,'product out of stock')
        return redirect('cart')
    
    else:
        


        cust=users.objects.get(email=request.session.get('name'))
        
        
        if Cart.objects.filter(product = procart ,user=cust):

            cartitem = Cart.objects.get(product = procart)
            cartitem.quantity += 1
            cartitem.save()
            
            # sin_price = Cart.objects.get(price = procart)
            # sin_price.save()


            
            # if  procart.quantity < cartitem.quantity:
            #     message.info(request,'item out of stock')
            return redirect('cart')
               

        else:    
            cartitem = Cart(product =procart ,user=cust,quantity=1)
            cartitem.save()
    
   
            return redirect('cart')


def update_cart(request):
    cust=users.objects.get(email=request.session.get('name'))
   
    if request.method == 'POST':
        total = 0
        sub_total=0
        item_id = request.POST['item_id']
      
        quantity = int(request.POST['quantity'])
        
        cart_item = Cart.objects.get(id=item_id)
        print('cart',cart_item)
      
        cart_item.quantity = quantity
        cart_item.save()
        print('poaa'+str(cart_item.quantity))

        print('gggggggggggg')
        
       
        cart = Cart.objects.filter(user = cust)
        for item in cart:
             total += item.product.price*item.quantity
             sub_total = cart_item.quantity * cart_item.product.price
            # sub_total = item.product.price*item.product.quantity
        return JsonResponse({
            'quantity' : quantity,
            'total' :total,
            'sub_total':sub_total
           
        })
    else:
        return jsonResponse({})

def remove_cart(request,id):
    # prodd = get_object_or_404(product, id=id)
    # if request.user.is_authenticated:
    #     cart_item=Cart.objects.get(product=prodd,user=request.user)
    # else:
    #     cart=Cart.objects.get(id=id)
    pdd = Cart.objects.get(id=id)
    pdd.delete()
    return redirect('cart')
    








    
def add_address(request):
    user=users.objects.get(email=request.session.get('name'))
    return render(request,'add_address.html',{'user':user})


def profile(request):
        
        #cust=users.objects.get(id=id)
       # addrs=Address.objects.all()
      
        if request.method=='POST':
            pincode=request.POST.get('pincode')
            phone=request.POST.get('Phone')
            print(phone)
            city=request.POST.get('city')
            state=request.POST.get('state')
            locality=request.POST.get('locality')
            flat=request.POST.get('flat')
            cust=users.objects.get(email=request.session.get('name'))
            Address.objects.create(pincode=pincode,city=city,state=state,locality=locality,flat=flat,user=cust,phone=phone)
            addrs=Address.objects.filter(user=cust)
            dp=UserProfilepic.objects.filter(user=cust).first()
            
            return render(request,'profile.html',{'cust':cust,'addrs':addrs,'dp':dp})
        
        else:
            cust=users.objects.get(email=request.session.get('name'))
            dp=UserProfilepic.objects.filter(user=cust).first()
            addrs=Address.objects.filter(user=cust)
            return render(request,'profile.html',{'cust':cust,'addrs':addrs,'dp':dp})

def deladdress(request,id):
    addr=Address.objects.get(id=id)
    addr.delete()
    cust=users.objects.get(email=request.session.get('name'))
    # context={
            
    #         'custs': cust.id
    #          }
    #return render(request,'profile.html',context)
    return redirect('profile')
def updateaddress(request,id):
    addr=Address.objects.get(id=id)
    if request.method=='POST':
         pincode=request.POST.get('pincode')
         city=request.POST.get('city')
         state=request.POST.get('state')
         locality=request.POST.get('locality')
         flat=request.POST.get('flat')
         phone=request.POST.get('phone')

         addr.phone=phone
         addr.pincode=pincode
         addr.city=city
         addr.state=state
         addr.locality=locality
         addr.flat=flat
         addr.save()
         cust=users.objects.get(email=request.session.get('name'))
         context={
            # 'prdct':prdct
            'custs': cust.id
             }

        
         return redirect('profile')
        #  return render(request,'profile.html',{'addr':addr})
    else:
        return render(request,'updateaddress.html',{'addr':addr})


def search_index(request):
    if request.method == 'POST':
        search = request.POST.get('quary')
        print(search)
        pro = products.objects.filter(name__icontains = search)
        print(pro)
        return render(request,'index.html',{'pro':pro})

def search_catogory(request):
    catgry=Category.objects.filter(status=0)
    bran=brands.objects.filter(status=0)
    
    if request.method == 'POST':
        search = request.POST.get('quary')
        print(search)
        pro = products.objects.filter(name__icontains = search)
        print(pro)
        context ={
            'catgry':catgry,
            'bran':bran,
            'pro':pro,
            
        }
        return render(request,'category.html',context)

def default(request,id):
    cust=users.objects.get(email=request.session.get('name'))
    addrs=Address.objects.filter(user=cust)
    defaultaddress=Address.objects.get(id=id)
    print(defaultaddress)
    defaultaddress.is_difault=True
    defaultaddress.save()

    for i in addrs:
        if i != defaultaddress:
            i.is_difault=False
            i.save()

    return redirect('checkout')

def checkout(request):
    total_price = 0
    discount = 0
    
    user = users.objects.get(email=request.session.get('name'))
    cart = Cart.objects.filter(user=user)
    addr = Address.objects.filter(user=user,is_difault=True)
    for item in cart:
        total_price += item.product.price * item.quantity 

    if 'coupons' in request.session:
        coupons = request.session['coupons']
        coup = Coupon.objects.get(coupon_code =coupons )
        print(coup)
        discount = coup.discount
        print(discount)
        messages.info(request,'')
        Usedcoupoon.objects.create(user = user,Coupon = coup)
    coupon = Coupon.objects.all()
    

    order_totel=total_price + 75
    shipping = 20
    payable =Decimal( (order_totel + shipping) - discount)
    print(payable,'payable')
    amount_in_paisa = int(payable * 100)  
    print(amount_in_paisa,'anount')
    # client = razorpay.Client(auth = (settings.key,settings.secret))
    client = razorpay.Client(auth = (settings.KEY,settings.SECRET))

    order_data = {
    'amount': amount_in_paisa,
    'currency': 'INR',
}


    payment = client.order.create(data=order_data)
    # context = {
    #     'order_totel':order_totel,
    #     'shipping':shipping,
    #     'payment':payment,


    # }
   
  
   
    print(payment)
    return render(request,'checkout.html',locals())


def applycoupon(request):
    if request.method == 'POST':
        coupons=request.POST.get('coupon')
        print(coupons)
        coup= Coupon.objects.filter(coupon_code=coupons)
        print(coup)


        if coup:

            request.session['coupons'] = coupons
            return redirect('checkout')

        else:
            print('fnjdnjvfd')
            messages.info(request,'invalid coupon')
            return redirect('checkout')

def placeorder(request):

    total=0
    discount=0
    catr_total_price = 0
    
    cust=users.objects.get(email=request.session.get('name'))
    addr = Address.objects.filter(user=cust,is_difault=True)
    
    payment_id = 'none'
    cart = Cart.objects.filter(user = cust)
    tracking_no=( random.randint(100000,999999))
   
    
    if 'payment_id' in  request.session:
            payment_mode ='Razorpay'
            payment_id= request.session['payment_id']
            print(payment_id)
           
            del request.session['payment_id']
    else:
        payment_mode ='cash on delivery'
    if 'coupons' in request.session:
        coupons = request.session['coupons']
        coup = Coupon.objects.get(coupon_code =coupons )
        discount = coup.discount
        del request.session['coupons']


    # for item in cart:
    #     catr_total_price = item.product.price * item.quantity 
    for item in cart:
            catr_total_price += item.product.price*item.quantity
            # sub_total = cart.quantity * cart.product.price
    

    order_totel=catr_total_price + 75
    shipping = 20
    payable = (order_totel + shipping) - discount

    print(payable)
   

    orders = order.objects.create(user = cust,
                                 total_price = payable,
                                 Addres = Address.objects.get(user=cust,is_difault=True),
                                 tracking_no = tracking_no,
                                 payment_mode = payment_mode,
                                 payment_id = payment_id,
                                 status = 'Confirmed',
                                


     )
    orders.save()
    for item in cart:

        odda=orderitem.objects.create(user = cust,
                                          orderit = orders,
                                          product = item.product,
                                          price = item.product.price,
                                          quantity = item.quantity,
                                          
                        
     )
       
        odda.save()
    


    for item in cart:
        prod = products.objects.filter(id=item.product.id).first()
         
        print(prod)
        prod.quantity = prod.quantity-item.quantity
        prod.save()
        # prod.delete()
    

    return render(request,'confirmation.html',locals())
    # return redirect('confirmation')




def view_order(request):
    
    cust=users.objects.get(email=request.session.get('name'))
    cart_items = order.objects.filter(user=cust)
    # print(cart_items,"tgfttgg")
    # for i in cart_items:
    #     print(i.id,"kooooooo")
    
    paginator = Paginator(cart_items,5)  # 10 items per page

    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
        print(page_data,'try')
    except PageNotAnInteger:
    # If page is not an integer, display the first page.
        page_data = paginator.page(1)
        print(page_data,'except1')
    except EmptyPage:
    # If page is out of range, display the last page of results.
        page_data = paginator.page(paginator.num_pages)
        print(page_data,'except2')

    except Exception as e:
    # Handle any other exceptions that may occur.
        print(f"An error occurred: {e}")
        page_data = paginator.page(1)

    context={
        'cart_items':page_data,
        'page_data':page_data,
        
        
    }
    
    
    return render(request,'view_order.html',context)

def single_order(request,id):
    cust=users.objects.get(email=request.session.get('name'))
  
    cart_items = orderitem.objects.filter(orderit=id)
    order_item = order.objects.get(id=id)
    print(order_item,'nowfan')
    
    print(cart_items,"pood12121")

    # orderr=order.objects.values_list('id', flat=True)
  
   # orders= order.objects.filter(id = orderr.orderit.id)

  
    

    context={
        'cart_items':cart_items,
        'order_item': order_item,
        
        
    }
    
    
    return render(request,'single_order.html', context)
    

def single_order_fetch(request,id):
    cust = users.objects.get(email=request.session.get('name'))
    cart_items = orderitem.objects.filter(orderit=id)
    order_item =order.objects.filter(id=id)
    print(order_item,'amal')
    print(cart_items,"uuuuu")
    d = []
    # orderr = orderitem.objects.get(orderit=id)
    for i in cart_items:
        a = i.product.name
        b = i.product.price
        c = i.quantity
        name = i.user.first_name
        
        tax = i.quantity * i.product.price
        tax = ((95/tax)*100 )
        d.append({"description":a,"quantity":c,"price":b,"tax-rate":tax} )

    for i in order_item:
        userAddress = i.Addres.city




   
   
    
    order_item = serializers.serialize('json', order_item)
    

    context = {
        'order_item':order_item,
        'd':d,
        'name':name,
        'userAddress':userAddress,
  
    }

    return JsonResponse(context)


def cancelorder(request,id):
    
    ordd =order.objects.get(id=id)
   
    print(ordd,"podddaaaa")
    
    
    ordd.status = "Cancelled"
    ordd.save()
    
 
   
    return redirect('view_order')



def return_order(request,id):
    
    ordd =order.objects.get(id=id)
   
    print(ordd)
    
    
    ordd.status = "Returned"
    ordd.save()
    
 
   
    return redirect('view_order')


@csrf_exempt
def payment_verification(request):
    
            try:
                  payment_id = request.POST.get('razorpay_payment_id','')
                  order_id = request.POST.get('razorpay_order_id','')
                  signature = request.POST.get('razorpay_signature','')
                  params_dict = {
                        'razorpay_payment_id':payment_id ,
                        'razorpay_order_id': order_id ,
                        'razorpay_signature':signature
                  }

                  print(payment_id,'id')
                  print(order_id,'order')
                  print(signature,'signat')
            except:
                  pass
            try:
                client.utility.verify_payment_signature(params_dict)
            except:
                  messages.info(request,'Payment Failed')
                  print('failed')
                  return redirect('checkout')
            
            
            request.session['payment_id'] = payment_id
            print(request.session['payment_id'])
           
            return redirect('placeorder')
      

def blog(request):
    return render(request,'blog.html')


def edit_profile(request):
    cust=users.objects.get(email=request.session.get('name'))
    try:
        user_profile = UserProfilepic.objects.get(user=cust)
    except UserProfilepic.DoesNotExist:
        user_profile = UserProfilepic(user=cust)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        messages.success(request, 'Profile picture updated successfully.')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})

def delete_profile_picture(request):
   cust=users.objects.get(email=request.session.get('name'))
   user_profile = UserProfilepic.objects.filter(user=cust.id).first()
   print(user_profile)
   user_profile.delete()
   return redirect('profile')


def cancelorder_raz(request,id):
    total=0
    
   
    cust=users.objects.get(email=request.session.get('name'))
    ordd =orderitem.objects.filter(id=id).filter(user=cust).first()
    ordrfnd= order.objects.get(id = id)
   
    paymet_id = ordrfnd.payment_id
    print(paymet_id,"kitto")
    total_price  = ordrfnd.total_price 
    print(total_price,"podaaaaa")
    print(paymet_id,'id got')
    client=razorpay.Client(auth=('rzp_test_6lIsuXRQbFxRKa','MxfeXY6XPZcXH76bx0m7ORs0'))
    payable =Decimal(total)
  
    print(str(paymet_id),'12121')
    h=float(payable)
    print(h)
    responce=client.payment.refund(paymet_id,h)
    status= 'Refund'
    ordrfnd.status=status
    ordrfnd.save()
    return redirect('view_order')

































