"""
URL configuration for blognews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signupview,name='signup'),
    path('login/',views.loginview,name='login'),
    path('editblog/',views.editblog,name='editblog'),
    path('createblog/',views.createblog,name='createblog'),
    path('deleteblog/<int:blog_id>/', views.deleteblog, name='deleteblog'),
    # path('api/blogs/', views.BlogListAPIView.as_view(), name='blog-list-api'),
    path('api/blogs/', views.BlogListCreateAPIView.as_view(), name='blog-list-create'),
     path('api/blogs/<int:pk>/', views.BlogRetrieveUpdateDestroyAPIView.as_view(), name='blog-detail'),
     path('blog/<int:pk>/', views.fullBlog, name='fullBlog'),
]
