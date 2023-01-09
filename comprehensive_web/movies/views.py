from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from members.models import Member
from .models import Movies
# Create your views here.
def all_movies(request, year=None):
    title = ""
    year = ""
    if 'get-title' in request.GET:
        title = request.GET['get-title']
        year = request.GET['year']
        
        
        if len(title) > 0:
            movies = Movies.objects.filter(title__icontains = title)
        
        # elif 'year' in request.GET:
        elif len(year) > 0:
            year = request.GET['year']
            movies = Movies.objects.filter(date__icontains = year)
            
            
        # elif 'get-title' in request.GET and 'year' in request.GET:
        elif len(title) > 0 and len(year) > 0:
            title = request.GET['get-title']
            year = request.GET['year']
            movies = Movies.objects.filter(title__icontains = title,
                                           date__icontains = year)
           
        else:
            movies = Movies.objects.all()
    else:
        movies = Movies.objects.all()
        
    
    if len(movies) == 0:
            messages.success(request, ("暫無資料"))
        
    
    
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

def test_m(request):
    year = '2022'
    # 
    # movies = Movies.objects.all()[:1]
    movies = Movies.objects.filter(date__icontains = year)
    c = movies.count()
    
    
    
    
    
    return render(request, 'test.html', locals())