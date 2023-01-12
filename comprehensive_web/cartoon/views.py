from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CarToon

from members.models import Member
# Create your views here.

def test(request):
    m = Member.objects.get(email = request.session['account'])
    n = m.username
    # # if 'select-sort' in request.GET:
    # #     select = request.GET['select-sort']
    # data = CarToon.objects.all()
    # # data.filter(year__icontains = '2021')
    # select = ''
    # title = ''
    # if request.method == 'GET':
    #     title = request.GET.get('get-title', '')
    #     select = request.GET.get('select-sort')
        
        
    #     if len(title) != 0:
    #         data = data.filter(subject__icontains = title)
    # if select == '1':
        
    #     data = data.order_by('-popularity')
    # elif select == '2':
    #     data = data.order_by('popularity')
    # else:
    #     data = data.order_by('id')
            
    # else:
    #     data = CarToon.objects.all()
    #     data = data.filter(year__icontains = '2021')
    # data = data.order_by('-popularity')[:10]
    # popularity = data.popularity
    # t = list()
    # t = t.append(data)
    # if '萬' in popularity:
    #     popularity = popularity.replace('萬', '0000')
    return render(request, 'test.html', locals())


def all_cartoon(request, year=None):
    title = ""
    year = ""
    select = 'id'
    data = CarToon.objects.all()
    if request.method == "GET":
    # if "get-title" in request.GET:
        year = request.GET.get('year', '')
        title = request.GET.get('get-title', '')
        select = request.GET.get('select-sort', 'id')
        
 
        if len(title) != 0 and len(year) != 0:
            data = data.filter(subject__icontains = title,
                                          year__icontains = year)
            
        elif len(title) != 0:
            data = data.filter(subject__icontains = title)
        
        elif len(year) != 0:            
            data = data.filter(year__icontains = year)

                    
        

    # else:
    #     data = CarToon.objects.all().order_by('id')
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


# def all_cartoon(request, year=None):
#     title = ""
#     year = ""
    
#     if "get-title" in request.GET:
#         year = request.GET.get('year', '')
#         title = request.GET['get-title']
#         # select = request.GET['select-sort']
        
 
#         if len(title) != 0 and len(year) != 0:
#             data = CarToon.objects.filter(subject__icontains = title,
#                                           year__icontains = year)
            
#         elif len(title) != 0:
#             data = CarToon.objects.filter(subject__icontains = title)
        
#         elif len(year) != 0:            
#             data = CarToon.objects.filter(year__icontains = year)            
        

#     # else:
#     #     data = CarToon.objects.all().order_by('id')
#     else:
#             data = CarToon.objects.all().order_by('id')
    
#     # if select == 'uid':
#     #     data = data.order_by('id')
        
#     # elif select == 'high':
#     #     data = data.order_by('')
    

    
    
        
#     paginator = Paginator(data, 20)
#     page = request.GET.get('page')
#     venues = paginator.get_page(page)
#     nums = 'a' * venues.paginator.num_pages
#     try:
#         data = paginator.page(page)
#     except PageNotAnInteger:
#         data = paginator.page(1)
#     except EmptyPage:
#         data = paginator.page(paginator).num_pages
        
#     all_page = paginator.get_page(page)
    
#     count = len(data)
#     if count == 0:
#         messages.success(request, ('查無資料'))
    
    
#     return render(request, 'cartoons.html', locals())
