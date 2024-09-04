"""
URL configuration for SocialMedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from Connect.views import *

admin.site.site_header = "Social_Media Admin"
admin.site.site_title = "Social_Media"
admin.site.index_title = "Welcome! to your very own Social Media.. Freely Express Yourself"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Login,name="login"),
    path("register/",Register,name="register"),
    path("reset_password/",Reset_Password,name="reset_pass"),
    path("in/<str:Username>/",UserDetails,name="UserProfile"),
    path("edit/<str:Username>/",Update_User_Details,name="UpdateUserProfile"),
    path("logout/",Logout,name="logout"),

    ################## Connections URLS ###################

    ##path("all_professionals/",All_Profession,name="professional") ## non-dynamic url,
    path("all_professionals/<str:what>/",All_Profession,name="professional"),

    ##path("professional_in_html/<str:what>/",All_Professional_filter_in_HTML,name="professional_inhtml"),
    path("connection/<str:action>/<int:u_id>/",Manage_your_connections,name="connections"),

    ################## Connection URLS ends ############################

    path("add_company/", Add_Company, name="addCompany"),
    path("your_company_details/",Company_Detail, name="company_detail"),

    ######## URLS for blogging Section #############
    path("new_blog_posted/",NewPost, name="new_post"),
    path("liked_blog/<int:blog_id>/<str:Username>/",Blogs_Liked,name="likedblogs"),
    path("disliked_blog/<int:blog_id>/<str:Username>/",Blogs_Disliked,name="dislikedblogs"),

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
