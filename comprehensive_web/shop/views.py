from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# 雜貨店
def GroceryStore(request):
    data = Product.objects.all()
    goodName = ""
    priceS = ""
    priceE = ""
    platform = 'all'
    item = 0
    
    if 'item' in request.GET:
    # if request.method == "GET":
        goodName = request.GET['p']
        priceS = request.GET['priceS']
        priceE = request.GET['priceE']
        item = request.GET['item']
        # platform = request.GET['platform']
        
        # 全部都搜尋
        if (item != "0" and len(goodName) != 0 and len(priceS) != 0 and len(priceE) != 0):
            data = data.filter(item = item,
                                subject__icontains = goodName,
                                price__gte = priceS,
                                price__lte=priceE,

                                )
        
        # 搜尋種類 + 商品名稱 + 最小
        elif (item != "0" and len(goodName) != 0 and len(priceS) != 0 and len(priceE) == 0):
            data = data.filter(item = item,
                                subject__icontains=goodName,
                                price__gte=priceS
                                )   
            
        # 搜尋種類 + 商品名稱 + 最大
        elif (item != "0" and len(goodName) != 0 and len(priceS) == 0 and len(priceE) != 0):
            data = data.filter(item = item,
                                subject__icontains=goodName,
                                price__gte=priceE
                                )   
            
        # 搜尋種類 + 商品名稱
        elif (item != "0" and len(goodName) != 0 and len(priceS) == 0 and len(priceE) == 0):
            data = data.filter(item = item,
                                subject__icontains=goodName
                                )
            
        # 種類 + 價格
        elif (item != "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) != 0):
            data = data.filter(item = item,
                                          price__gte=priceS,
                                          price__lte=priceE)
            
        # 商品 + 價格
        elif (item == "0" and len(goodName) != 0 and len(priceS) != 0 and len(priceE) != 0):
            data = data.filter(subject__icontains = goodName,
                                          price__gte=priceS,
                                          price__lte=priceE)

        # 商品 + 價格
        elif (item == "0" and len(goodName) != 0 and len(priceS) != 0 and len(priceE) == 0):
            data = data.filter(subject__icontains = goodName,
                                          price__gte=priceS)
            
        # 價格 最小與最大
        elif (item == "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) != 0):
            data = data.filter(price__gte=priceS,
                                          price__lte=priceE)
        
        # 搜尋大於多少的價格商品
        elif (item == "0" and len(goodName) == 0 and len(priceS) != 0 and len(priceE) == 0):
            data = data.filter(price__gte=priceS)
            
        # 搜尋小於多少的價格商品
        elif (item == "0" and len(goodName) == 0 and len(priceS) == 0 and len(priceE) != 0):
            data = data.filter(price__lte=priceE)
        
        # 搜尋商品名稱
        elif (item == "0" and len(goodName) != 0 and len(priceS) == 0 and len(priceE) == 0):
            data = data.filter(subject__icontains=goodName)
        
        # 搜尋類別
        elif (item != "0" and len(goodName) == 0 and len(priceS) == 0 and len(priceE) == 0):
            data = data.filter(item = item)
            
        # # 搜尋類別
        # elif (item == "0" and len(goodName) == 0 and len(priceS) == 0 and len(priceE) == 0 and platform != 'all'):
        #     data = data.filter(platform = platform)
            
        else: 
            data = data.all()
            
    else:    
        data = data.all()
    

        
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