from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CarToon

from members.models import Member
# Create your views here.


def all_cartoon(request, year=None):
    title = ""
    year = ""
    select = 'id'
    data = CarToon.objects.all()
    if request.method == "GET":
    # if "get-title" in request.GET:
        year = request.GET.get('year', '')
        title = request.GET.get('get-title', '')
        select = request.GET.get('select_sort', 'uid')
        
 
        if len(title) != 0 and len(year) != 0:
            data = data.filter(subject__icontains = title,
                                          year__icontains = year)
            
        elif len(title) != 0:
            data = data.filter(subject__icontains = title)
        
        elif len(year) != 0:            
            data = data.filter(year__icontains = year)

        
    else:
        data = CarToon.objects.all().order_by('id')
    
    if select == 'low':
        data = data.order_by('popularity')
    elif select == 'high':
        data = data.order_by('-popularity')
    elif select == 'news':
        data = data.order_by('-year')
    elif select == 'old':
        data = data.order_by('year')
        
    else:
        data = data.order_by('id')
    
    
    
        
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
    
    count = len(data)
    if count == 0:
        messages.success(request, ('查無資料'))
    
    
    return render(request, 'cartoons.html', locals())


