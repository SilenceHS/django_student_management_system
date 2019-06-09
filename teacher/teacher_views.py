import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import openpyxl
import json
# Create your views here.
from python_end.Student import Student
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
    sql = "select * from Course where teacher_id= %s"
    cursor.execute(sql,teacher_id)
    c = cursor.fetchall()
    courses=[]
    for i in c:
        courses.append(Course(i[0],i[2]))
    return courses
def addcourseaction(request):
    sql="insert into Course (teacher_id,name) values(%s,%s)"
    cursor = connection.cursor()
    cursor.execute(sql,(request.session.get('teacherid'),request.POST['classname']))

    courses=getAllCourse(request)
    file=request.FILES.get("file", None)
    wb = openpyxl.load_workbook(file)
    sheet=wb.active
    for i in range(1,sheet.max_row+1):
        sql2 = "insert into `student-course` (student_id,student_name,course_id) values(%s,%s,%s)"
        cursor.execute(sql2, (sheet.cell(i,1).value,sheet.cell(i,2).value,courses[len(courses) - 1].ID))
    return redirect('/teacher/coursedetail?id='+str(courses[len(courses) - 1].ID))

def coursedetailview(request):
    adict=get_teacher_dict(request)
    adict['nowclick']=int(request.GET['id'])
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM `student-course` where course_id=%s"
    cursor.execute(sql,request.GET['id'])
    c = cursor.fetchall()
    adict['studentcount']=int(c[0][0])
    return render(request,'teacher/courseinfo.html',adict)
def addcourseview(request):
    return render(request, 'teacher/addcourse.html',get_teacher_dict(request))

def deletecourse(request):
    cursor = connection.cursor()
    sql = "delete  FROM `student-course` where course_id=%s;"
    cursor.execute(sql,(request.POST['opid']))
    sql2="delete  FROM `course` where id=%s;"
    cursor.execute(sql2, (request.POST['opid']))
    return redirect('index.html')
def studentdetailview(request):
    adict = get_teacher_dict(request)
    adict['nowclick'] = int(request.GET['id'])
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM `student-course` where course_id=%s"
    cursor.execute(sql, request.GET['id'])
    c = cursor.fetchall()
    adict['studentcount'] = int(c[0][0])
    students=[]
    sql = "SELECT * FROM `student-course` where course_id=%s"
    cursor.execute(sql, request.GET['id'])
    c = cursor.fetchall()


    adict['list'] = [int(x) for x in range(1, len(c))]
    sql = "select count(*) from `participation`,`student-participation` where `participation`.id=`student-participation`.participation_id " \
          "and participation.course_id=%s"
    cursor.execute(sql, request.GET['id'])
    d=cursor.fetchall()


    for i in range(len(c)):
        sql = "select count(*),sum(score) from `student-course`,`course-student` where `student-course`.id=`course-student`.course_selectID and " \
              "`student-course`.course_id=%s and  `student-course`.student_id=%s"
        cursor.execute(sql, (request.GET['id'],c[i][1]))
        e = cursor.fetchall()
        s=Student(c[i][1],c[i][2],d[0][0],e[0][0],e[0][1])
        students.append(s)
    students=sorted(students,key=lambda x:int(x.ID))
    adict['student']=students
    return render(request, 'teacher/studentdetail.html', adict)


