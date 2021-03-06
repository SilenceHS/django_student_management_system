from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import json
import hashlib


def md5(s):  # md5加密
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))
    return md5.hexdigest()


def hello(request):  # 首页
    return render(request, 'home/index.html')


def loginstu(request):  # 登录
    result = {'ifok': 'false'}
    a = request.POST.get('stu-id')
    b = request.POST.get('stu-psw')
    print(b)
    b = md5(b)
    print(a)
    print(b)
    cursor = connection.cursor()
    sql = "select * from Student where ID=%s and Password=%s"
    cursor.execute(sql,(a,b))
    c = cursor.fetchall()
    if len(c) != 0:
        result['ifok'] = 'true'
        request.session['stuid'] = c[0][0]
        request.session['stuname'] = c[0][1]
        #request.session.set_expiry(60)
    return HttpResponse(json.dumps(result))


def loginteacher(request):  # 登录
    result = {'ifok': 'false'}
    a = request.POST.get('teacher-id')
    b = request.POST.get('teacher-psw')
    print(b)
    b = md5(b)
    print(a)
    print(b)
    cursor = connection.cursor()
    sql = "select * from Teacher where ID=%s and Password=%s"
    cursor.execute(sql,(a,b))
    c = cursor.fetchall()
    print(c)
    if len(c) != 0:
        request.session['teacherid']=c[0][0]
        request.session['teachername'] = c[0][1]
        #request.session.set_expiry(60)
        result['ifok'] = 'true'
    return HttpResponse(json.dumps(result))


def checkstu(request):  # 在页面中使用ajax检查是否账号已经注册过
    a = request.POST.get('stu-id')
    l = {'ifok': '0'}
    if a == "":
        return HttpResponse(json.dumps(l))
    cursor = connection.cursor()
    cursor.execute("select ID from Student where ID=%s",(a,))
    b = cursor.fetchall()
    if len(b) == 0:
        l['ifok'] = 'true'
    else:
        l['ifok'] = 'false'
    return HttpResponse(json.dumps(l))  # 返回结果


def checkteacher(request):  # 在页面中使用ajax检查是否账号已经注册过
    a = request.POST.get('teacher-id')
    l = {'ifok': '0'}
    if a == "":
        return HttpResponse(json.dumps(l))
    cursor = connection.cursor()
    sql = "select ID from Teacher where ID=%s"
    cursor.execute(sql,(a,))
    b = cursor.fetchall()
    if len(b) == 0:
        l['ifok'] = 'true'
    else:
        l['ifok'] = 'false'
    return HttpResponse(json.dumps(l))  # 返回结果


def regstu(request):  # 注册学生账号跳转到此
    result = {'ifok': 'false'}
    id = request.POST.get('stu-id')
    name = request.POST.get('stu-name')
    major = request.POST.get('stu-major')
    psw = request.POST.get('stu-psw')
    # 密码使用md5加密储存,更加安全
    psw = md5(psw)
    cursor = connection.cursor()
    sql = "insert into Student values(%s,%s,%s,%s)"
    try:
        cursor.execute(sql,(id, name, psw, major))
        result = {'ifok': 'true'}
    except BaseException:
        pass
    return HttpResponse(json.dumps(result))


def regteacher(request):  # 注册教师账号跳转到此
    result = {'ifok': 'false'}
    id = request.POST.get('teacher-id')
    name = request.POST.get('teacher-name')
    psw = request.POST.get('teacher-psw')
    # 密码使用md5加密储存,更加安全
    psw = md5(psw)
    cursor = connection.cursor()
    sql = "insert into Teacher values(%s,%s,%s)"
    try:
        cursor.execute(sql,(id, name, psw))
        result = {'ifok': 'true'}
    except BaseException:
        pass
    return HttpResponse(json.dumps(result))
