from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from members.models import Member
from .models import Movies
# Create your views here.
def all_movies(request, year=None):
    title = ""
    year = ""
    if 'get-title' in request.GET:
        title = request.GET['get-title']
        
        movies = Movies.objects.filter(title__icontains = title)

    else:
        movies = Movies.objects.all()
    
    
    if year == '2022':
        movies = Movies.objects.filter(date__icontains = year)
        
    
    
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

def test(request):
    # year = '2022'
    # movies = Movies.objects.all().order_by('id')[:1]
    # d = movies.date[0][4]
    # for i in movies:
    #     date = i[4]
    
    d = Member.objects.get(email = request.session['account'])
    
    
    
    return render(request, 'test.html', locals())