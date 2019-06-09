from django.conf.urls import url
from teacher import teacher_views
urlpatterns = [
    url(r'^$|^index.html$',teacher_views.index),
    url(r'^getMyCourse$',teacher_views.getAllCourse),
    url(r'^addcourse.html$',teacher_views.addcourseview),
    url(r'^addcourse.action$',teacher_views.addcourseaction),
    url(r'^coursedetail$',teacher_views.coursedetailview),
    url(r'^delete.action$',teacher_views.deletecourse),
    url(r'^studentdetail$',teacher_views.studentdetailview),
]