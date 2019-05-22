from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    stuid = request.session.get('stuid')
    stuname=request.session.get('stuname')
    if stuid:
        return render(request,'student/index.html',{'stuid':stuid,'stuname':stuname})
    else:
        return redirect('/index.html')
