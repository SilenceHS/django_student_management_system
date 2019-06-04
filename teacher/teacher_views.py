from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import json
# Create your views here.
from python_end.Course import Course

#打包返回教师信息的方法
def get_teacher_dict(request):
    teacherid = request.session.get('teacherid')
    teachername = request.session.get('teachername')
    course = getAllCourse(request)
    return {'teacherid':teacherid,'teachername':teachername,"courses":course}


def index(request):
    teacherid=request.session.get('teacherid')
    teachername=request.session.get('teachername')
    course=getAllCourse(request)
    if teacherid:
        return render(request,'teacher/teacherhome.html',get_teacher_dict(request))
    else:
        return redirect('/index.html')
def getAllCourse(request):
    cursor = connection.cursor()
    tablename='Course'
    teacher_id=request.session['teacherid']
    print(teacher_id)
    sql = "select * from {0} where teacher_id='{1}'  ".format(tablename,teacher_id)
    cursor.execute(sql)
    c = cursor.fetchall()
    courses=[]
    for i in c:
        courses.append(Course(i[0],i[2]))
    return courses
def addcourseview(request):
    return render(request, 'teacher/addcourse.html',get_teacher_dict(request))

