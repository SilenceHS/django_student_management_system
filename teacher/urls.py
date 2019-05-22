from django.conf.urls import url
from teacher import teacher_views
urlpatterns = [
    url(r'^$',teacher_views.index),
    url(r'^getMyCourse$',teacher_views.getAllCourse),
]