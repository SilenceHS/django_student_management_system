from django.conf.urls import url
from teacher import teacher_views
urlpatterns = [
    url(r'^$|^index.html$',teacher_views.index),

    url(r'^getMyCourse$',teacher_views.getAllCourse),
    url(r'^addcourse.html$',teacher_views.addcourseview),
]