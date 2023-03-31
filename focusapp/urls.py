from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
   
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('',views.index,name='index'),
    path('logout',views.logout,name='logout'),
    # path('CustomPasswordResetView',views.CustomPasswordResetView,name='CustomPasswordResetView'),
    path('search_index',views.search_index,name='search_index'),
    path('search_catogory',views.search_catogory,name='search_catogory'),
    path('blog',views.blog,name='blog'),
    path('ForgetPassword',views.ForgetPassword,name='ForgetPassword'),
    path('password_otp',views.password_otp,name='password_otp'),
    path('repassword',views.repassword,name='repassword'),
#   ..................................forgot pasword................................ 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('category',views.category,name='category'),
    path('filter_category/<int:id>',views.filter_category,name='filter_category'),
    path('single_product/<int:id>',views.single_product,name='single_product'),
    path('single_order_fetch/<int:id>',views.single_order_fetch,name='single_order_fetch'),

    path('cart',views.cart,name='cart'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
    path('update_cart',views.update_cart,name='update_cart'),
    path('verify_login/',views.verify_login,name='verify_login'),
    # ..........................................wishlist........................................
    path('view_wishlist',views.view_wishlist,name='view_wishlist'),
    path('add_to_wish/<int:id>',views.add_to_wish,name='add_to_wish'),
    path('remove_wish/<int:id>',views.remove_wish,name='remove_wish'),

    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,profile,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    path('profile',views.profile,name='profile'),
    path('add_address',views.add_address,name='add_address'),
    path('deladdress/<int:id>',views.deladdress,name='deladdress'),
    path('updateaddress/<int:id>',views.updateaddress,name='updateaddress'),
    path('default/<int:id>',views.default,name='default'),
    # .........................................checkout..........................................
    path('checkout',views.checkout,name='checkout'),
    # path('confirmation/<int:id>',views.confirmation,name='confirmation'),
    path('applycoupon',views.applycoupon,name='applycoupon'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('payment_verification',views.payment_verification,name='payment_verification'),
    # ............................................order............................................
    path('view_order',views.view_order,name='view_order'),
    path('single_order/<int:id>',views.single_order,name='single_order'),
    path('cancelorder/<int:id>',views.cancelorder,name='cancelorder'),
    path('return_order/<int:id>',views.return_order,name='return_order'),
    path('cancelorder_raz/<int:id>',views.cancelorder_raz, name='cancelorder_raz'),


    # .............................................dp...............................................
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('delete_profile_picture',views.delete_profile_picture,name='delete_profile_picture'),
] 
