from django.urls import path
from .import views


urlpatterns = [
 
    path('',views.admin,name='admin'),
    path('admin_index',views.admin_index,name='admin_index'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('add_category',views.add_category,name='add_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('category_management',views.category_management,name='category_management'),
    path('update_category/<int:id>',views.update_category,name='update_category'),
    path('search_category',views.search_category,name='search_category'),
    # ...................................user..........................................
    path('user_view',views.user_view,name='user_view'),
    path('blockuser/<int:pk>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),
    path('delete/<int:id>',views.delete,name='delete'),
    # ...................................products.......................................
    path('view_products',views.view_products,name='view_products'),
    path('add_products',views.add_products,name='add_products'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('update_products/<int:id>',views.update_products,name='update_products'),




    # ................................brand......................................
    path('add_brand',views.add_brand,name='add_brand'),
    path('delete_brand/<int:id>',views.delete_brand,name='delete_brand'),
    path('view_brand',views.view_brand,name='view_brand'),
    path('update_brand/<int:id>',views.update_brand,name='update_brand'),
    path('search_brand',views.search_brand,name='search_brand'),



    # ................................view_coupon...................................
      path('view_coupon',views.view_coupon,name='view_coupon'),
      path('add_coupon',views.add_coupon,name='add_coupon'),
      path('active_cop/<int:id>',views.active_cop,name='active_cop'),
      path('deactive_cop/<int:id>',views.deactive_cop,name='deactive_cop'),
      path('delete_cop/<int:id>',views.delete_cop,name='delete_cop'),

      # .................................order........................................

      path('view_orders',views.view_orders,name='view_orders'),
      path('shipped_orders/<int:id>',views.shipped_orders,name='shipped_orders'),
      path('out_of_delivary_orders/<int:id>',views.out_of_delivary_orders,name='out_of_delivary_orders'),
      path('deliverd_order/<int:id>',views.deliverd_order,name='deliverd_order'),

      #...................................dashbrord....................................

      path('chart',views.chart,name='chart'),
      path('view_chart',views.view_chart,name='view_chart'),
      path('sales_chart_data',views.sales_chart_data,name='sales_chart_data'),
      path('detials/<int:id>',views.detials,name='detials'),
      

      



    

]