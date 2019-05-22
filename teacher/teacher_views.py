from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import json
# Create your views here.
from python_end.Course import Course


def index(request):
    teacherid=request.session.get('teacherid')
    teachername=request.session.get('teachername')
    course=getAllCourse(request)
    if teacherid:
        return render(request,'teacher/teacherhome.html',{'teacherid':teacherid,'teachername':teachername,"courses":course})
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

