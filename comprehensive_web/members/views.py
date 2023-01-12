from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from members import forms

from .models import Member

import hashlib
# Create your views here.

# def test(request):
#         postform = forms.PostForm()
        
#         return render(request, 'test.html', locals())



# def login(request):
#     msg = ""
#     account = ""
#     password = ""
#     if request.method == 'POST':
#         account = request.POST['email']
#         password = request.POST['pwd']
#         postform = forms.PostForm(request.POST)
#         if postform.is_valid():
#             password = hashlib.sha3_256(password.encode(encoding='utf-8')).hexdigest()
            
#             obj = Member.objects.filter(email = account,
#                                         password = password).count()
            
#             if obj == 1:
#                 request.session['account'] = account
#                 request.session['isAlive'] = True
                
#                 return HttpResponseRedirect('/')
                
            
#             else:
#                 messages.success(request, ("帳密錯誤請重新輸入"))
#                 # msg = "帳密錯誤請重新輸入"
#                 return render(request, 'login.html', locals())
#         else:
#             messages.success(request, ("驗證未通過!X﹏X"))
#             postform = forms.PostForm()
#             return render(request, 'login.html', {'postform': postform})
        
#     else:
#         if "account" in request.session and "isAlive" in request.session:
#             return HttpResponseRedirect("/all_cartoon")
        
#         else:
#             postform = forms.PostForm()
#             messages.success(request, ("歡迎登入ヽ(✿ﾟ▽ﾟ)ノ"))
#             msg = "歡迎光臨"
#             return render(request, 'login.html', locals())

def login(request):
    msg = ""
    
    if "email" in request.POST:
        
        account = request.POST['email']
        password = request.POST['pwd']
        
        
        password = hashlib.sha3_256(password.encode(encoding='utf-8')).hexdigest()
        
        obj = Member.objects.filter(email = account,
                                    password = password).count()
        
        if obj == 1:
            request.session['account'] = account
            request.session['isAlive'] = True
            
            return HttpResponseRedirect('/')
            
        
        else:
            messages.success(request, ("帳密錯誤請重新輸入"))
            # msg = "帳密錯誤請重新輸入"
            return render(request, 'login.html', locals())
    
    else:
        if "account" in request.session and "isAlive" in request.session:
            return HttpResponseRedirect("/all_cartoon")
        
        else:
            messages.success(request, ("歡迎登入ヽ(✿ﾟ▽ﾟ)ノ"))
            msg = "歡迎光臨"
            return render(request, 'login.html', locals())


def register(request):
    msg = ""
    account = ""
    username = ""
    password = ""
    birthday = ""
    sex = ""
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
            
            
            return HttpResponseRedirect('/login')
        else:
            # return render(request, 'register.html', locals())
            messages.success(request, ("Email已註冊過，請換一個~(*￣rǒ￣)"))
            msg="Email已註冊"
    
    return render(request, 'register.html', locals())

def logout(request):
    del request.session['account']
    del request.session['isAlive']
    
    return HttpResponseRedirect('/')

    
def member_manage(request):
    old_pwd = ""
    new_pwd = ""
    if "account" in request.session and "isAlive" in request.session:
        
        if 'old_password' in request.POST and 'new_password' in request.POST:
            old_pwd = request.POST['old_password']
            new_pwd = request.POST['new_password']
            
            old_pwd = hashlib.sha3_256(old_pwd.encode(encoding='utf-8')).hexdigest()
            new_pwd = hashlib.sha3_256(new_pwd.encode(encoding='utf-8')).hexdigest()
            
            obj = Member.objects.filter(email = request.session['account'], password = old_pwd).count()
            
            if obj > 0:
                member = Member.objects.get(email = request.session['account'])
                member.password = new_pwd
                member.save()
                msg = "密碼變更完成"
                # return redirect('/memberSetting')
                
            else:
                msg = "密碼輸入錯誤"
                
                
            
        
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


