"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from Class import urls as class_urls
from student_view import urls as student_urls
from teacher_view import urls as teacher_urls
from student_view import views as student_views

urlpatterns = [
    path('', student_views.home_page, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'Class/', include(class_urls)),
    url(r'student/', include(student_urls)),
    url(r'teacher/', include(teacher_urls)),
    url(r'accounts/profile', student_views.profile_page, name='student_profile_view')
]
