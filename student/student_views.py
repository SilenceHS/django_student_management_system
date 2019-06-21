from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import json
# Create your views here.

def index(request):
    stuid = request.session.get('stuid')
    stuname=request.session.get('stuname')
    cursor = connection.cursor()
    sql = "select course.id,course.name,`now-course`.start_date, `now-course`.end_date from course,`now-course` where end_date is null and `now-course`.course_id=course.id and course.id in (select course_id from `student-course` where student_id=%s)"
    cursor.execute(sql, stuid)
    a=cursor.fetchall()
    alist=[]
    for i in a:
        adict={'id':i[0],'name':i[1],'status':'上课中'}
        sql2='select * from participation where course_id=%s'
        cursor.execute(sql2,i[0])
        b=cursor.fetchall()
        for k in b:
            if k[2] is not None and k[3] is None:
                adict['status']='签到中'
                adict['pid']=k[0]
        alist.append(adict)
    if stuid:
        return render(request,'student/base.html',{'course':alist})
    else:
        return redirect('/index.html')

def stupart(request):
    result = {'ifok': 'false'}
    stuid = request.session.get('stuid')
    pid=request.POST.get('pid')
    print(stuid)
    print(pid)
    print(".................")
    cursor = connection.cursor()
    sql = "select count(*) from `student-participation` where student_id=%s and participation_id=%s"
    cursor.execute(sql, (stuid,pid))
    a=cursor.fetchall()
    if a[0][0]>0:
        return HttpResponse(json.dumps(result))
    else:
        sql = "insert into `student-participation` values(%s , %s)"
        cursor.execute(sql, (stuid, pid))
        result['ifok']='true'
        return HttpResponse(json.dumps(result))
def putquestionview(request):
    return render(request,'student/question.html',{'cid':request.GET['cid']})
def putquestion(request):
    cid=request.POST.get('cid')
    content=request.POST.get('content')
    cursor = connection.cursor()
    sql = "insert into question (student_id,course_id,content) values(%s,%s,%s) "
    cursor.execute(sql, (request.session.get('stuid'), cid,content))
    result = {'ifok': 'true'}
    return HttpResponse(json.dumps(result))
