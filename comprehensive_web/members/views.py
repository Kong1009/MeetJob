from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Member

import hashlib
# Create your views here.


def login(request):
    msg = ""
    if "email" in request.POST:
        account = request.POST['email']
        password = request.POST['pwd']
        
        # password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        password = hashlib.sha3_256(password.encode(encoding='utf-8')).hexdigest()
        
        obj = Member.objects.filter(email = account,
                                    password = password).count()
        
        if obj > 0:
            request.session['account'] = account
            request.session['isAlive'] = True
            
            return HttpResponseRedirect('/')
            
        
        else:
            msg = "帳密錯誤請重新輸入"
            return render(request, 'login.html', locals())
            # return HttpResponseRedirect('/all_cartoon')
        
    
    else:
        if "account" in request.session and "isAlive" in request.session:
            return HttpResponseRedirect("/all_cartoon")
        
        else:
            msg = "歡迎光臨"
            return render(request, 'login.html', locals())


def register(request):
    msg = ""
    
    if "email" in request.POST:
        account = request.POST['email']
        username = request.POST['username']
        password = request.POST['pwd']
        birthday = request.POST['birthday']
        sex = request.POST['sex']
        
        password = hashlib.sha3_256(password.encode(encoding='utf-8')).hexdigest()
        
        obj = Member.objects.filter(email = account).count()
        
        if obj == 0:
            member = Member.objects.create(email = account,
                                           username = username,
                                           password = password,
                                           birthday = birthday,
                                           sex = sex)
            
            member.save()
            msg = "註冊完成"
            
            return HttpResponseRedirect('/login')
        else:
            msg="Email已註冊"
    
    return render(request, 'register.html', locals())

def logout(request):
    del request.session['account']
    del request.session['isAlive']
    
    return HttpResponseRedirect('/')

    
def member_manage(request):
    if "account" in request.session and "isAlive" in request.session:
        
        data = Member.objects.get(email = request.session['account'])
        # data = Member.objects.filter(email = member)
        return render(request, 'memberManage.html', locals())
    else:
        return redirect('/login/')
    


def forget_pwd(request):
    
    if 'email' in request.POST:
        account = request.POST['email']
        data = Member.objects.filter(email = account).count()
        
        if data == 1:
            return render(request, 'forget_pwd.html')
        else:
            return HttpResponseRedirect('/login')


