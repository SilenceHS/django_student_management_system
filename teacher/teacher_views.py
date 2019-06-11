import os
import time
from django.utils.http import urlquote
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import openpyxl
import json
# Create your views here.
from python_end.Student import Student
from python_end.Course import Course
from django.utils.encoding import escape_uri_path
import os
#打包返回教师信息的方法
def get_teacher_dict(request):
    teacherid = request.session.get('teacherid')
    teachername = request.session.get('teachername')
    course = getAllCourse(request)
    return {'teacherid':teacherid,'teachername':teachername,"courses":course}


def get_students(request):
    adict = get_teacher_dict(request)
    adict['nowclick'] = int(request.GET['id'])
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM `student-course` where course_id=%s"
    cursor.execute(sql, request.GET['id'])
    c = cursor.fetchall()
    adict['studentcount'] = int(c[0][0])
    students = []
    sql = "SELECT * FROM `student-course` where course_id=%s"
    cursor.execute(sql, request.GET['id'])
    c = cursor.fetchall()
    adict['list'] = [int(x) for x in range(1, len(c))]
    sql = "select count(*) from `participation`,`student-participation` where `participation`.id=`student-participation`.participation_id " \
          "and participation.course_id=%s"
    cursor.execute(sql, request.GET['id'])
    d = cursor.fetchall()
    for i in range(len(c)):
        sql = "select count(*),sum(score) from `student-course`,`course-student` where `student-course`.id=`course-student`.course_selectID and " \
              "`student-course`.course_id=%s and  `student-course`.student_id=%s"
        cursor.execute(sql, (request.GET['id'], c[i][1]))
        e = cursor.fetchall()
        s = Student(c[i][1], c[i][2], d[0][0], e[0][0], e[0][1])
        students.append(s)
    students = sorted(students, key=lambda x: int(x.ID))
    adict['student'] = students
    return adict
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
    return render(request, 'teacher/studentdetail.html', get_students(request))
def downstu(request):
    filename = time.strftime("%Y-%m-%d-")
    id=request.GET['id']
    teacher_id=request.session['teacherid']
    cursor = connection.cursor()
    sql = "select name from Course where teacher_id= %s and id=%s"
    cursor.execute(sql,(teacher_id,id))
    c = cursor.fetchall()
    filename+=c[0][0]+"成绩汇总.xlsx"
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.cell(1,1).value='学号'
    sheet.cell(1, 2).value = '姓名'
    sheet.cell(1, 3).value = '出勤次数'
    sheet.cell(1, 4).value = '老师提问次数'
    sheet.cell(1, 5).value = '提问总分'
    a=get_students(request)
    students=a["student"]
    for i in range(len(students)):
        sheet.cell(i+2, 1).value = students[i].ID
        sheet.cell(i+2, 2).value = students[i].name
        sheet.cell(i+2, 3).value = students[i].pcount
        sheet.cell(i+2, 4).value = students[i].qcount
        sheet.cell(i+2, 5).value = students[i].qscore
    wb.save("temp/"+filename)
    with open('temp/'+filename, 'rb') as model_excel:
        result = model_excel.read()
    response = HttpResponse(result)
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    os.remove("temp/"+filename)
    return response