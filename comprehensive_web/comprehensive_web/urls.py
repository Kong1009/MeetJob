"""comprehensive_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from movies.views import all_movies
from cartoon.views import all_cartoon
from members.views import member_manage, register,  logout, login, forget_pwd
from shop.views import GroceryStore
from shopcart.views import addtocart, cart, cartorder, cartok, cartordercheck, myorder, ECPayCredit
from contact.views import contact
from home.views import index
from photos.views import uploadFile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('home/', index),
    
    # 動漫區
    path('all_cartoon/', all_cartoon),
    
    # 電影區
    path('all_movie/', all_movies),
    
    # 會員專區
    path('memberSetting/', member_manage),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('forget_pwd/', forget_pwd),
    
    # 商店
    path('general_store/', GroceryStore),
    
    # 購物車
    path('cart/', cart),
    path('addtocart/<str:ctype>/', addtocart),
    path('addtocart/<str:ctype>/<int:productid>/', addtocart),
    path('cartorder/', cartorder),
    path('cartok/', cartok),
    path('cartordercheck/', cartordercheck),
    path('myorder/', myorder),
    
    # 信用卡
    path('creditcard/', ECPayCredit),
    
    # 照片牆
    path('photos/', uploadFile),

    # 聯絡我們
    path('contact/', contact),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

