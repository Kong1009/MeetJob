from django.shortcuts import render, redirect
from .forms import UploadModelForm
from .models import Photo
from django.contrib import messages
# Create your views here.


    

def uploadFile(request):
    photos = Photo.objects.all()
    form = UploadModelForm()
    
    if 'account' in request.session and 'isAlive' in request.session:
    
        if request.method == "POST":
            form = UploadModelForm(request.POST, request.FILES)
            
            if form.is_valid():
                form.save()
                
                return redirect('/photos')
        
        context = {
            'photo': photos,
            'form': form
            }
        messages.success(request, ("親愛的會員您好!歡迎上傳圖片!!"))
    else:
        messages.success(request, ("請先登入會員，才能上傳圖片!!!"))
        # msg = "請先登入會員，才能上傳圖片!!!"
    
    
    return render(request, 'photos.html', locals())

