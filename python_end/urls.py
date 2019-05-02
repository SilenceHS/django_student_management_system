"""python_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf.urls import url
from . import view
from teacher import teacher_views
from student import student_views
urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$|^index.html$',view.hello),
    url(r'^loginstu',view.loginstu),
    url(r'^checkstu',view.checkstu),
    url(r'^checkteacher',view.checkteacher),
    url(r'^regstu',view.regstu),
    url(r'^regteacher',view.regteacher),
    url(r'^loginteacher',view.loginteacher),
    url(r'^teacher$',teacher_views.index),
    url(r'^student$',student_views.index)
]
