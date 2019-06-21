from django.conf.urls import url
from student import student_views
urlpatterns = [
    url(r'^$|index.html',student_views.index),
    url(r'^stupart$',student_views.stupart),
    url(r'^putquestionview$',student_views.putquestionview),
    url(r'^putquestion$',student_views.putquestion),

]