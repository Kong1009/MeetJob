from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.



# 雜貨店
def GroceryStore(request):
    goodName = ""
    priceS = ""
    priceE = ""
    item = 0
    
    if 'item' in request.GET:
        goodName = request.GET['p']
        priceS = request.GET['priceS']
        priceE = request.GET['priceE']
        item = request.GET['item']        
        
        # 全部都搜尋
        if (item != "0" and len(goodName) != 0 and len(priceS) != 0 and len(priceE) != 0):
            data = Product.objects.filter(item = item,
                                          subject__icontains = goodName,
                                          price__gt = priceS,
                                          price__lte=priceE
                                          )
            
        # 搜尋種類 + 商品名稱
        elif (item != "0" and len(goodName) != 0 and len(priceS) == 0 and len(priceE) == 0):
            data = Product.objects.filter(item = item,
                                          subject__icontains=goodName
                                          )
            
        # 種類 + 價格
        elif (item != "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) != 0):
            data = Product.objects.filter(item = item,
                                          price__gt=priceS,
                                          price__lte=priceE)
            
        elif (item == "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) != 0):
            data = Product.objects.filter(price__gt=priceS,
                                          price__lte=priceE)
        
        # 搜尋大於多少的價格商品
        elif (item == "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) == 0):
            data = Product.objects.filter(price__gt=priceS)
            
        # 搜尋小於多少的價格商品
        elif (item == "0" and len(goodName) == 0 and len(priceS) == 0 and len(priceE) != 0):
            data = Product.objects.filter(price__lte=priceE)
        
        # 搜尋商品名稱
        elif (item == "0" and len(goodName) != 0 and len(priceS) == 0 and len(priceE) == 0):
            data = Product.objects.filter(subject__icontains=goodName)
            
        elif (item != "0" and len(goodName) == 0 and len(priceS) == 0 and len(priceE) == 0):
            data = Product.objects.filter(item = item)
            
        else:    
            data = Product.objects.all()
            
    else:    
        data = Product.objects.all()
    

        
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
        msg = "查無商品"
    
    return render(request, 'shop.html', locals())