from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
import json
import hashlib


def md5(s):  # md5加密
    md5 = hashlib.md5()
    md5.update(s.encode(encoding='utf-8'))
    return md5.hexdigest()


def hello(request):  # 首页
    return render(request, 'home/index.html')


def login(request):#登录
    a = request.GET['stu-id']
    b = request.GET['stu-psw']
    cursor = connection.cursor()
    cursor.execute("select * from Student")
    c = cursor.fetchall()
    return HttpResponse("进入")


def checkstu(request):  # 在页面中使用ajax检查是否账号已经注册过
    a = request.POST.get('stu-id')
    l = {'ifok': '0'}
    if a == "":
        return HttpResponse(json.dumps(l))
    cursor = connection.cursor()
    cursor.execute("select ID from Student where ID=" + a)
    b = cursor.fetchall()
    if len(b) == 0:
        l['ifok'] = 'true'
    else:
        l['ifok'] = 'false'
    return HttpResponse(json.dumps(l))#返回结果

def checkteacher(request):  # 在页面中使用ajax检查是否账号已经注册过
    a = request.POST.get('teacher-id')
    l = {'ifok': '0'}
    if a == "":
        return HttpResponse(json.dumps(l))
    cursor = connection.cursor()
    sql="select ID from Teacher where ID='{0}'".format(a)
    cursor.execute(sql)
    b = cursor.fetchall()
    if len(b) == 0:
        l['ifok'] = 'true'
    else:
        l['ifok'] = 'false'
    return HttpResponse(json.dumps(l))#返回结果
def regstu(request):  # 注册学生账号跳转到此
    result = {'ifok': 'false'}
    id = request.POST.get('stu-id')
    name = request.POST.get('stu-name')
    major = request.POST.get('stu-major')
    psw = request.POST.get('stu-psw')
    # 密码使用md5加密储存,更加安全
    psw=md5(psw)
    cursor = connection.cursor()
    sql = "insert into Student values('{0}','{1}','{2}','{3}')".format(id, name, psw, major)
    try:
        cursor.execute(sql)
        result = {'ifok': 'true'}
    except BaseException:
        pass
    return HttpResponse(json.dumps(result))
def regteacher(request):# 注册教师账号跳转到此
    result = {'ifok': 'false'}
    id = request.POST.get('teacher-id')
    name = request.POST.get('teacher-name')
    psw = request.POST.get('teacher-psw')
    # 密码使用md5加密储存,更加安全
    psw=md5(psw)
    cursor = connection.cursor()
    sql = "insert into Teacher values('{0}','{1}','{2}')".format(id, name, psw)
    try:
        cursor.execute(sql)
        result = {'ifok': 'true'}
    except BaseException:
        pass
    return HttpResponse(json.dumps(result))
