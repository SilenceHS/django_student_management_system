from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
import json
import hashlib

def hello(request):#首页
    return render(request,'home/index.html')
def login(request):
    a=request.GET['stu-id']
    b=request.GET['stu-psw']
    cursor=connection.cursor()
    cursor.execute("select * from Student")
    c=cursor.fetchall()
    print(c)
    return HttpResponse("进入")
def checkstu(request):#在页面中使用ajax检查是否账号已经注册过
    a=request.POST.get('stu-id')
    print(a)
    l = {'ifok': '0'}
    if a=="":
        return HttpResponse(json.dumps(l))
    cursor = connection.cursor()
    cursor.execute("select ID from Student where ID="+a)
    b=cursor.fetchall()
    print(b)
    print(len(b))
    if len(b)==0:
        l['ifok']='true'
    else:
        l['ifok']='false'
    return HttpResponse(json.dumps(l))
def regstu(request):#注册学生账号跳转到此
    result={'ifok':'false'}
    id = request.POST.get('stu-id')
    name=request.POST.get('stu-name')
    major=request.POST.get('stu-major')
    psw=request.POST.get('stu-psw')
    #密码使用md5加密储存,更加安全
    md5=hashlib.md5()
    md5.update(psw.encode(encoding='utf-8'))
    psw=md5.hexdigest()
    print(psw)
    cursor = connection.cursor()
    sql="insert into Student values('{0}','{1}','{2}','{3}')".format(id,name,psw,major)
    try:
        cursor.execute(sql)
        result = {'ifok': 'true'}
    except BaseException:
        pass
    return HttpResponse(json.dumps(result))
