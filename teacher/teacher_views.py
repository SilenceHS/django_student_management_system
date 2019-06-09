import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import openpyxl
import json
# Create your views here.
from python_end.Course import Course

#打包返回教师信息的方法
def get_teacher_dict(request):
    teacherid = request.session.get('teacherid')
    teachername = request.session.get('teachername')
    course = getAllCourse(request)
    return {'teacherid':teacherid,'teachername':teachername,"courses":course}

######################################

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
def addcourseaction(request):

    sql="insert into Course (teacher_id,name) values(%s,%s)"
    cursor = connection.cursor()
    cursor.execute(sql,(request.session.get('teacherid'),request.POST['classname']))
    file=request.FILES.get("file", None)
    wb = openpyxl.load_workbook(file)
    sheet=wb.active
    for i in range(1,sheet.max_row+1):
        print(sheet.cell(i,1).value,sheet.cell(i,2).value)
    return redirect('/teacher/index.html')

def coursedetailview(request):
    adict=get_teacher_dict(request)
    adict['nowclick']=int(request.GET['id'])
    return render(request,'teacher/courseinfo.html',adict)
def addcourseview(request):
    return render(request, 'teacher/addcourse.html',get_teacher_dict(request))



