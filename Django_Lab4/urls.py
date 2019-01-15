"""Django_Lab4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from Lab4 import views
from django.views.generic import TemplateView
from  Lab4 import FilesList

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='index_final.html', extra_context=FilesList.Get2ListOfFile())), стрый обработчик index
    path('', views.IndexPage.as_view()),
    path('About', TemplateView.as_view(template_name='About.html')),
    path('registration', views.Registration.as_view()),
    path('login', views.LogIn.as_view()),
    path('logout', views.LogOut.as_view()),
    re_path(r'^music/(?P<artist>.{1,50})/(?P<song>.{1,50})', views.TrackPage.as_view()),
    re_path(r'^', TemplateView.as_view(template_name='404.html')),
]
