from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Movies
# Create your views here.
def all_movies(request, year=None):
    title = ""
    year = ""
    select = "uid"
    movies = Movies.objects.all()
    
    # 判斷 是否有值帶入
    if request.method == 'GET':
    # if 'get-title' in request.GET:
        title = request.GET.get('get-title', '')
        year = request.GET.get('year', '')
        select = request.GET.get('select-sort', 'uid')
        
        if len(title) != 0 and len(year) != 0:
            movies = movies.filter(title__icontains = title,
                                           date__icontains = year)
            
        elif len(title) != 0:
            movies = movies.filter(title__icontains = title)
        
        
        elif len(year) != 0:
            year = request.GET['year']
            movies = movies.filter(date__icontains = year)
        
        else:
            movies = Movies.objects.all()
    else:
        movies = Movies.objects.all()
        
        
    # 判斷 排序方式
    if select == 'evaluation_low':
        movies = movies.order_by('evaluation')
    elif select == 'evaluation_high':
        movies = movies.order_by('-evaluation')
    elif select == 'news':
        movies = movies.order_by('-date')
    elif select == 'old':
        movies = movies.order_by('date')
    else:
        movies = movies.order_by('id')

    # 檢查有無資料
    if len(movies) == 0:
            messages.success(request, ("暫無資料"))
        
    
    # 分頁
    paginator = Paginator(movies, 20)
    page = request.GET.get('page')
    venues = paginator.get_page(page)
    nums = 'a' * venues.paginator.num_pages
    
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator).num_pages
        
        
    all_page = paginator.get_page(page)
        
        
    return render(request, 'movie.html', locals())

