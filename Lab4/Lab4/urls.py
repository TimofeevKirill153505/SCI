"""
URL configuration for Lab4 project.

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

from django.contrib.auth import views as auth_views

from mainapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.redirect_index),
    path("main", views.index),
    path("login", auth_views.LoginView.as_view(template_name="login.html")),
    path("catalog", views.catalog),
    path("order", views.order),
    path('registration', views.registration),
    path('user', views.personal),
    path("logout", views.logout_out),
    path('cancel', views.cancel),
    path('staff', views.staff),
    path('userinfo', views.userinfo),
    path('activate', views.activate),
    path('cancelOrder', views.cancelOrder),
    path('diagram', views.diagram),
    path('statistics', views.statistics),
    path('addmodel', views.addmodel),
    path('addauto', views.addauto),
    path('searchuser', views.searchuser),
    path('editmodel', views.editmodel),
    path('modellist', views.modellist),
    path('delete', views.delete),
    path('autolist', views.autolist),
    path('editauto', views.editauto),
    path('news', views.news),
    path('reviews',views.reviews),
    path('faq', views.faq),
    path('discounts', views.discounts),
    path('politic', views.politic),
    path('contacts', views.contacts),
    path('about', views.about),
    path('newspage', views.newspage),
    path("funnypage", views.funnypage)
]
