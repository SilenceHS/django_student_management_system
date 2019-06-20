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
    url(r'^down_stufile$',teacher_views.downstu),
    url(r'^pardetail$',teacher_views.pardetailview),
    url(r'^startclass$',teacher_views.start_class),
    url(r'^endclass$',teacher_views.end_class),
    url(r'^startparaction$',teacher_views.start_participation),
    url(r'^endparaction$',teacher_views.end_participation),
    url(r'^courseware$', teacher_views.coursewareview),
    url(r'^upload$', teacher_views.upload),
    url(r'^deleteware$', teacher_views.deleteware),
]