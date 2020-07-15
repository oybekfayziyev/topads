"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views as token_views
from . import apis
urlpatterns = [

    # PROFILE API
    path('api/users/', apis.UserApi.as_view()),
    
    # PRODUCT API
    path('api/products/', apis.ProductApi.as_view({'get' : 'list'})),
    path('api/product/<slug>/', apis.ProductApi.as_view({
                                                         'get' : 'retrieve',
                                                         'put' : 'update'})),
    path('api/product/', apis.ProductApi.as_view({'post' : 'create'})),  
    
    # AUTHENTICATION API
    path('api/account/register/', apis.RegisterApi.as_view()),  
    path('api/account/login/', token_views.obtain_auth_token),   # TOKEN AUTHENTICATION
    path('api/account/logout/', apis.LogoutApi.as_view()),

    # CATEGORY
    path('api/product/get/categories/', apis.GetCategoryApi.as_view({'get' : 'list'})),
    path('api/product/get/category/<pk>/',apis.GetCategoryApi.as_view({'get':'retrieve'})),
    path('api/product/update/category/<pk>/', apis.CategoryApi.as_view({'put' : 'update'})),
    path('api/product/add/category/', apis.CategoryApi.as_view({'post' : 'create'})),

    #SUBCATEGORY
    path('api/product/get/subcategories/', apis.GetSubcategoryApi.as_view({'get' : 'list'})),
    path('api/product/get/subcategory/<pk>/',apis.GetSubcategoryApi.as_view({'get':'retrieve'})),
    path('api/product/update/subcategory/<pk>/', apis.SubcategoryApi.as_view({'put':'update'})),
    path('api/product/add/subcategory/', apis.SubcategoryApi.as_view({'post':'create'})),
        
    #COMMENT
    path('api/product/comment/<pk>/', apis.CommentApi.as_view({'get':'retrieve','post':'create'})),
    path('api/product/comment/<p_id>/<c_id>/', apis.CommentApi.as_view({'delete':'drop'})),
    
    # LIKES AND DISLIKES
    path('api/product/like/<pk>/', apis.LikeApi.as_view({'get':'retrieve'})),
    path('api/product/dislike/<pk>/', apis.DislikeApi.as_view({'get':'retrieve'})),
    
]
