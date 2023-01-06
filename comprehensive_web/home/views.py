from django.shortcuts import render
from movies.models import Movies
from cartoon.models import CarToon
# Create your views here.
def index(request):
    movie_data = Movies.objects.all().order_by('?')[:5]
    cartoon_data = CarToon.objects.all().order_by('?')[:5]
    
    # return render(request, 'home.html', locals())
    return render(request, 'home.html', {'movie_data': movie_data, 'cartoon_data': cartoon_data})