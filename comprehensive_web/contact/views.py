from django.shortcuts import render
from .models import Contact
# Create your views here.
def contact(request):
    msg = ''
    title = ''
    username = ''
    info = ''
    if 'title' in request.POST and 'username' in request.POST:
        title = request.POST['title']
        username = request.POST['username']
        info = request.POST['info']

        data = Contact.objects.create(title = title, username = username, info = info)
        msg = "您的訊息已收到"
        
    elif 'title' not in request.POST:
        msg = "標題未輸入"
    
    elif 'username' not in request.POST:
        msg = "使用者名稱未輸入"
    
    
        
    return render(request, 'contact.html', locals())