from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from shopcart import models
from shop.models import Product
from members.models import Member
from datetime import datetime

from django.utils.html import format_html

import os
basedir = os.path.dirname(__file__) # 抓取預設目錄位置
file = os.path.join(basedir, 'ecpay_payment_sdk.py')
# 崁入ECPay 的SDK
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Create your views here.

cartlist = list() # 購物車內容
customname = "" # 客戶姓名
customphone  = "" # 客戶電話
customaddress = "" # 客戶地址
customemail = "" # 客戶email

orderTotal = 0 #消費金額
goodsTitle = list() # 存放放入購物車的商品名稱

# 這個是加入到購物車中，並未將商品資訊寫入至資料庫中
def addtocart(request, ctype = None, productid = None):
    global cartlist
    
    if ctype == "add": # 將商品加入至購物車中
        product = Product.objects.get(id = productid) # 會用get 是因為帶入的產品ID 一定有在資料表中(如果不確定要用filter)
        flag = True # 預設購物車中沒有相同的商品，表示購物車內這個商品不存在
        
        # 檢查購物車中的商品是否有重複
        for unit in cartlist:
            if product.subject == unit[0]: # 表示有這個商品
                unit[2] = str(int(unit[2]) + 1) # 數量在加1
                unit[3] = str(int(unit[3]) + int(product.price)) # 累計金額
                flag = False # 表示商品之前已經加入至購物車中
                break
            
            # 這裡的的索引值是對應model.py的 DetailModel欄位
            # unit[0] 商品名稱
            # unit[1] 價格
            # unit[2] 數量
            # unit[3] 總價
        
        if flag: # 在購物車中沒有此商品
            templist = list()
            templist.append(product.subject)
            templist.append(str(product.price))
            templist.append('1')
            templist.append(str(product.price))
            cartlist.append(templist)
            
        # 將購物車內容存入到Session 中 Session是可以將資料儲存在伺服器端，當瀏覽器關閉時，資料就會被清除
        request.session['cartlist'] = cartlist        
        return redirect('/cart/') # 跳轉至此網頁
    
    # 修改購物車數量
    elif ctype == "update":
        n = 0
        for unit in cartlist: # 將購物車內容抓出來，並修改數量和總價
            amount = request.POST.get('qty' + str(n), '1')
            if len(amount) == 0:
                amount = '1'
            if int(amount) <= 0:
                amount = '1'
                
            unit[2] = amount
            unit[3] = str(int(unit[1]) * int(unit[2]) )
            n += 1
            
        request.session['cartlist'] = cartlist
        
        return redirect('/cart/')
    
    # 清空購物車
    elif ctype == "empty":
        cartlist = list() # 重新指向空的串列
        request.session['cartlist'] = cartlist    
        return redirect('/cart/')

    # 刪除單一品項
    elif ctype == "remove":
        del cartlist[int(productid)] # 將放入的商品索引值刪除
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
        
    # redirect 直接跳到指定的網址去，並沒有帶任何參數過去
    # render 跳到指定的網址去，並將要求 (request) 將參數內容傳過去給網頁
    
        
    
# 顯示購物車內容用
def cart(request):
    global cartlist
    allcart = cartlist
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    
    grandtotal = total + 100 # 預測運費為100元
    return render(request, 'cart.html', locals())
    



# 結帳
def cartorder(request):
    # 當要結帳時，是要登入後，才可以結帳。 先不做登入的結帳
    
    # 12/1 補上登入
    if "account" in request.session and "isAlive" in request.session:
        global cartlist, customname, customphone, customaddress, customemail
        
        total = 0
        allcart = cartlist
        for unit in cartlist:
            total += int(unit[3])
        
        grandtotal = total + 100 # 加運費
        
        # member_data = Member.objects.filter(email = request.session['account'])
        # customname = member_data.name
        name = customname
        phone = customphone
        address = customaddress
        email = request.session['account']
        
        return render(request, 'cartorder.html', locals())
    
    else:
        return HttpResponseRedirect('/login')


# 以確認資料並送出。所以會將訂單寫入資料庫
def cartok(request):
    global cartlist, customname, customphone, customaddress, customemail
    global orderTotal, goodsTitle
    
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    
    grandtotal = total + 100
    orderTotal = grandtotal
    
    customname = request.POST.get('cuName', '')
    customphone = request.POST.get('cuPhone', '')
    customaddress = request.POST.get('cuAddress', '')
    customemail = request.POST.get('cuEmail', '')
    paytype = request.POST.get('payType')
    
    # 新增資料至訂單資料表中(資料庫)
    unitorder = models.OrdersModel.objects.create(subtotal = total,
                                                  shipping = 100,
                                                  total_amount = grandtotal,
                                                  customername = customname,
                                                  customerphone = customphone,
                                                  customeraddress = customaddress,
                                                  customeremail = customemail,
                                                  paytype = paytype)
    
    # 要將各個的商品新增到 明細表
    for unit in cartlist:
        goodsTitle.append(unit[0]) # 將要買的商品名稱新增至 goodsTitle中
        total = int(unit[1]) * int(unit[2])
        unitordetail = models.DetailModel.objects.create(dorder = unitorder,
                                                      pname = unit[0],
                                                      unitprice = unit[1],
                                                      quantity = unit[2],
                                                      dtotal = total)

    orderid = unitorder.id # 取得訂單編號
    name = unitorder.customername
    email = unitorder.customeremail
    cartlist = list()
    request.session['cartlist'] = cartlist
    
    # 判斷付款方式
    if paytype == "信用卡":
        # return HttpResponseRedirect('/creditcard') # 導至信用卡頁面
        return redirect('/creditcard/')
    else:        
        return render(request, 'cartok.html', locals())
    
    

# 訂單完成後，可以做訂單查詢用的
def cartordercheck(request):
    orderid = request.GET.get('orderid', '')
    customemail = request.GET.get('customemail', '')
    
    if orderid == '' and customemail == '':
        nosearch = 1
    else:
        order = models.OrdersModel.objects.filter(id=orderid).first() # 抓第一筆資料
    
        if order == None:
            notfound = 1
        else:
            details = models.DetailModel.objects.filter(dorder=order)
    return render(request, 'cartordercheck.html', locals())
        
    

def myorder(request):
    # 判斷 SESSION 是否存在
    # 抓出使用者的購買紀錄
    if "account" in request.session and "isAlive" in request.session:
        email = request.session['account']
        
        # order = models.OrdersModel.objects.filter(customeremail = email)
        order = models.OrdersModel.objects.filter(customeremail = email)
        return render(request, 'myorder.html', locals())
    else:
        return HttpResponseRedirect('/login')
    

# 綠界信用卡
def ECPayCredit(request):
    global goodsTitle
    
    title = ""
    
    for i in goodsTitle:
        title += i + "#" # 加 #號 是因為商品若為多個時，要用# 隔開
                        # '商品1#商品2'
        
    
    order_params = {
    'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
    'StoreID': '',
    'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    'PaymentType': 'aio',
    'TotalAmount': orderTotal,
    'TradeDesc': 'Kong-MeetJob訂單',
    'ItemName': title,
    'ReturnURL': 'https://www.lccnet.com.tw/lccnet', # 回傳網址
    'ChoosePayment': 'Credit',
    'ClientBackURL': 'https://www.lccnet.com.tw/lccnet', # 回到客戶端
    'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
    'Remark': '交易備註',
    'ChooseSubPayment': '',
    'OrderResultURL': 'https://www.lccnet.com.tw/lccnet', # 訂單完成導回此處
    'NeedExtraPaidInfo': 'Y',
    'DeviceSource': '',
    'IgnorePayment': '',
    'PlatformID': '',
    'InvoiceMark': 'N',
    'CustomField1': '',
    'CustomField2': '',
    'CustomField3': '',
    'CustomField4': '',
    'EncryptType': 1,
    }
    
    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }
    
    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }
    
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }
    
    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    
    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    
    # 合併發票參數
    order_params.update(inv_params)
    
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
    
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        
        html = format_html(html) # 格式化html，將文字的html 轉換為網頁html
        return render(request, 'paycredit.html', locals())
        # print(html)
    except Exception as error:
        print('An exception happened: ' + str(error))
