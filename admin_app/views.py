from django.shortcuts import render,redirect
# from django.contrib.auth.models import User,auth
from user_area.models import users
# User = settings.AUTH_USER_MODEL
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from focusapp.models import *
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models.functions import TruncMonth


# from chartit import DataPool, plotly





# Create your views here.

def admin(request):
    if 'user' in request.session:
        return redirect('admin_index')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST["password"]
        user = authenticate(email=email,password=password)
        if user is not None:

            if user.is_superuser:

                request.session['user']=email
            
                return redirect('admin_index')
        else:

            return render(request,'admin_login.html')

    return render(request,'admin_login.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_index(request):

    if 'user' in request.session:
        objs = users.objects.all()
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



def category_management(request):
   
    cata=Category.objects.all()
    print('category_management')
    return render(request,'category_management.html',{'cata':cata})

  # context =  { 'category':Category.objects.all()}

     
  
  # return render(request,'category_management.html',context)    


def add_category(request):
    #cata = Category.objects.get(id=id) 

    if request.method == 'POST':
        
            category_name = request.POST.get('category_name')
            
            if  Category.objects.filter(name= category_name).exists():
                messages.success(request, 'Category already exists')
                return redirect('add_category')
            else:
            # category = Category.objects.Create(category_name=category_name)
            # category.save()
                cata = Category(name=category_name)
                cata.save()
                return redirect('category_management')
    return render(request, 'add_category.html')
def delete_category(request,id):
    my= Category.objects.get(id=id)
    my.delete()
    return redirect('category_management')

def update_category(request,id):
    carup = Category.objects.get(id=id)
    if request.method =='POST':
        name = request.POST.get('name')
        carup.name = name
        carup.save()
        return redirect('category_management')

    else:
        return render(request,'update_category.html',{'carup':carup})

def search_category(request):
    if request.method == 'POST':
        search = request.POST.get('quary')
        print(search)
        cata = Category.objects.filter(name = search)
        print(cata)
        return render(request,'category_management.html',{'cata':cata})

    # else:
    #     return render(request,'category_management.html')

    

    



#usermngmt----------------
def user_view(request):
    user=users.objects.all()
    context={'user':user}
    return render(request,"users.html",context)

def block_user(request,pk):
    user = users.objects.get(id=pk)
    user.is_active = False
    user.save()
    print('user blocked')
    return redirect('user_view')




def unblock_user(request,id):
    user = users.objects.get(id= id)
    user.is_active  = True
    user.save()
    print('user is active')
    return redirect('user_view')
 
def delete(request,id):
    my= users.objects.get(id=id)
    my.delete()
    return redirect('user_view')



    # ...................................................................products...................................................................
    
def view_products(request):
    prod = products.objects.all()


    return render(request,'view_products.html',{'prod': prod})

def add_products(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        discription = request.POST.get('discription')
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')
        category = request.POST.get('a')
        brand = request.POST.get('b')
        category = Category.objects.get(id=category)
        brand = brands.objects.get(id=brand)
        product = products(name=name,
                            price=price,
                            description=discription,
                            image_1=image_1,
                            image_2=image_2,
                            image_3=image_3,
                            size = size,
                            quantity = quantity,
                            category=category,
                            brans=brand)
        product.save()
        # prod = Product.objects.select_related('category','brand').all()
       
        return redirect('view_products')
    else:
        categories = Category.objects.all()
        brand = brands.objects.all()

        return render(request,'add_products.html',{'categories': categories,'brand':brand} )

def delete_product(request,id):
    my= products.objects.get(id=id)
    my.delete()
    return redirect('view_products')


def update_products(request,id):
    podd = products.objects.get(id=id)
    if request.method =='POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        discription = request.POST.get('discription')
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')
        category = request.POST.get('a')
        brand = request.POST.get('b')
        category = Category.objects.get(id=category)
        brand = brands.objects.get(id=brand)
        podd.name = name
        podd.price = price
        podd.discription = discription
        podd.image_1 = image_1
        podd.image_2 = image_2
        podd.image_3 = image_3
        podd.quantity = quantity
        podd.size = size
        podd.category = category
        podd.brand = brand
        podd.save()
        # return render(request,'view_products.html')
        return redirect('view_products')
    else:
        categories = Category.objects.all()
        brand = brands.objects.all()
        return render(request,'update_products.html',{'podd':podd,'categories': categories,'brand':brand})



        


def view_brand(request):
    cata=brands.objects.all()

    return render(request,'view_brand.html',{'cata':cata})

  


def add_brand(request):
   

    if request.method == 'POST':
        
            brand_name = request.POST.get('brand_name')
            
            if  brands.objects.filter(name= brand_name).exists():
                messages.success(request, 'this brand already exists')
                return redirect('add_brand')
            else:
           
                cata = brands(name=brand_name)
                cata.save()
                return redirect('view_brand')
    return render(request, 'add_brand.html')
def delete_brand(request,id):
    my= brands.objects.get(id=id)
    my.delete()
    return redirect('view_brand')

def update_brand(request,id):
    bran = brands.objects.get(id=id)
    if request.method =='POST':
        
        name = request.POST.get('name')
        bran.name = name
        bran.save()
        return redirect('view_brand')

    else:
        return render(request,'update_brand.html',{'bran':bran})

def search_brand(request):
    if request.method == 'POST':
        search = request.POST.get('quary')
        print(search)
        cata = brands.objects.filter(name__icontains = search)
        print(cata)
        return render(request,'view_brand.html',{'cata':cata})

    else:
        return render(request,'view_brand.html')

def view_coupon(request):
    coup=Coupon.objects.all()
    return render(request,'view_coupon.html',{'coup':coup})

def add_coupon(request):
    form = CouponForm()

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_coupon')
    else:
        form = CouponForm()

    context = {
        'form':form
    }
    return render(request,'couponadd.html', context)

def active_cop(request,id):
    coup = Coupon.objects.get(id=id)
    print(coup)
    coup.is_active =True
    coup.save()
    return redirect('view_coupon')

def deactive_cop(request,id):
    coup = Coupon.objects.get(id=id)
    coup.is_active =False
    coup.save()
    return redirect('view_coupon')

def delete_cop(request,id):
    coup = Coupon.objects.get(id=id)
    coup.delete()
    return redirect('view_coupon')


def view_orders(request):
    ord = orderitem.objects.all()
    return render(request,'order.html',{'ord':ord})

def shipped_orders(request,id):
    ord = orderitem.objects.get(id=id)
    ord.orderit.status = "Shipped"
    ord.orderit.save()
    

    return redirect('view_orders')

def out_of_delivary_orders(request,id):
    ord = orderitem.objects.get(id=id)
    ord.orderit.status = "Out_for_delivery"
    ord.orderit.save()
    

    return redirect('view_orders')

def deliverd_order(request,id):
    ord = orderitem.objects.get(id=id)
    ord.orderit.status = "Delivered"
    ord.orderit.save()
    

    return redirect('view_orders')


def chart(request):
    user=users.objects.all().count()   
    ordercount=order.objects.all().count() 
    orderlist=orderitem.objects.all()
    order_uu=order.objects.all()
   
    orderlists = orderitem.objects.filter(Q(orderit__status ='Delivered'))
    orderli = orderitem.objects.filter(Q(orderit__status ='Delivered')).count()
    Grandtotal=0
    for item in orderlists:
    
        total=item.orderit.total_price
        Grandtotal=+total+Grandtotal
    product = []
    qty = []
    
    for items in orderlist:
        if items.product.name in product:
            index = product.index(items.product.name)
            qty[index] += items.quantity

        else:
            product.append(items.product.name)
            qty.append(items.quantity)
    # context = {
    # 'product': product,
    # 'qty': qty,
    # 'Grandtotal': Grandtotal,
    # 'user': user,
    # 'ordercount': ordercount,
    #         }

    

    return render(request,'admin_index.html',locals())







def view_chart(request):

    top_products = orderitem.objects.values('product').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:3]

   
    top_product_ids = [product['product'] for product in top_products]

  
    top_product_names = []
    top_product_sales = []
    for product in top_products:
        top_product_names.append(products.objects.get(id=product['product']).name)
        top_product_sales.append(product['total_sales'])

    
    orders = orderitem.objects.all()

  

    chart_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'datasets': []
    }

   
    for i in range(len(top_product_names)):
        dataset = {
            'label': top_product_names[i],
            'data': [],
            'backgroundColor': f'rgba(235, 22, 22, .{7 - i * 2})'
        }
        for j in range(12):
            sales = orders.filter(product=top_product_ids[i], orderit__created_at__month=j+1).aggregate(Sum('quantity'))['quantity__sum']
            dataset['data'].append(sales or 0)
        chart_data['datasets'].append(dataset)
        

    # return render(request, 'sales_chart.html', {'chart_data': chart_data})
    return JsonResponse({'chart_data': chart_data,'sdsd':'sdd'})

def sales_chart_data(request):
    sales_data = order.objects.filter(status='Delivered').annotate( month=TruncMonth('created_at')).values('month').annotate(total_sales=Sum('total_price')).order_by('month')
   
    labels = []
    sales = []
    for sale in sales_data:
        
        sales.append(sale['total_sales'])
    # print(labels)
    # print(sales)
    data = {
        'labels': labels,
        'sales': sales,
    }
    return JsonResponse(data)

def detials(request,id):
    
  
    cart_items = orderitem.objects.filter(orderit=id)

    order_item = order.objects.get(id=id)
    print(order_item,'nowfan')
    
    print(cart_items,"pood12121")

    # orderr=order.objects.values_list('id', flat=True)
    # orderr = orderitem.objects.get(id=id)
    # print(orderr,'kiiiiiiiiiiiiiiiiiiiiiiiii')
    # order_item=orderr.objects.filter(id = orderr.orderit.id)
    # print(order_item,'muhamed')

  
    

    context={
        'cart_items':cart_items,
        'order_item': order_item,
        
        
    }
    
    
    return render(request,'detials.html', context)



























    






