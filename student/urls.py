from django.conf.urls import url
from student import student_views
urlpatterns = [
    url(r'^.*$',student_views.index),

]