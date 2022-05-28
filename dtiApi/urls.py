from knox import views as knox_views
from django.urls import path
from . import views

urlpatterns = [
    #for api
    path('api/products', views.getData),
    path('api/products/basicnecessities', views.getProductsBasic),
    path('api/products/primecommodities', views.getProductsPrime),
    path('api/products/concern', views.getConcern),
    path('api/products/complaints', views.sendConcern),
    path('api/pdf', views.getPDF),
    path('api/login', views.api_login),
    path('api/current_user', views.current_user),
    #path('products/category', views.passCategory)

    #For Generics
    path('', views.home, name='home'),
    path('login', views.doLogin, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('products', views.products, name='products'),
    path('add_products', views.add_products, name='add_products'),
    path('add_products_resource', views.add_products_resource, name='add_products_resource'),
    path('update_price/<product_id>', views.update_price, name='update_price'),
    path('delete_product/<product_id>', views.delete_products, name='delete'),
    path('complains', views.complains, name='complains'),
    path('data', views.data, name='data'),
    path('data_save', views.data_save, name='data_save'),
    path('categories', views.categories, name='categories'),
    path('categories_save', views.categories_save, name='categories_save'),
    path('accounts', views.accounts, name='accounts'),
    path('save_account', views.save_account, name='save_account'),
]
