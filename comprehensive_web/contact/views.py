from django.shortcuts import render
from .models import Contact
from django.contrib import messages
# Create your views here.



def contact(request, sendmsg=None):
    msg = ''
    title = ''
    username = ''
    info = ''
    if sendmsg == 'sendmsg':
        if 'title' in request.POST and 'username' in request.POST:
            title = request.POST['title']
            username = request.POST['username']
            info = request.POST['info']
    
            data = Contact.objects.create(title = title, username = username, info = info)
            messages.success(request, ('您的訊息已收到'))
            msg = "您的訊息已收到"
            
        elif 'title' not in request.POST:
            msg = "標題未輸入"
            messages.success(request, ('標題未輸入'))
        
        elif 'username' not in request.POST:
            msg = "使用者名稱未輸入"
            messages.success(request, ('使用者名稱未輸入'))
            
        return render(request, 'contact.html', locals())
    else:
        
        messages.success(request, ('您好!'))
        return render(request, 'contact.html')