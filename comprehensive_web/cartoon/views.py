from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CarToon
# Create your views here.

def all_cartoon(request):
    title = ""
    
    if "get-title" in request.GET:
        subject = request.GET['get-title']
        
        data = CarToon.objects.filter(subject__icontains = subject)
        
    else:
    
        data = CarToon.objects.all().order_by()
        
    paginator = Paginator(data, 20)
    page = request.GET.get('page')
    venues = paginator.get_page(page)
    nums = 'a' * venues.paginator.num_pages
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator).num_pages
        
    all_page = paginator.get_page(page)
    
    
    
    
    return render(request, 'all_cartoon.html', locals())
