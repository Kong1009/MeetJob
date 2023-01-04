from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Movies
# Create your views here.
def all_movies(request):
    title = ""
    
    if 'get-title' in request.GET:
        title = request.GET['get-title']
        
        movies = Movies.objects.filter(title__icontains = title)
        
    else:
        movies = Movies.objects.all()
    
    
    
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