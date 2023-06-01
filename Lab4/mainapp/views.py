from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from requests import get
import django.http.request as req
from .models import CarModel, ClientModel, AutoModel, OrderModel, DiscountModel, PenaltyModel
from .forms import RegistrationForm, OrderForm
from .forms import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import datetime
import re
import plotly.graph_objects as pltl
import logging as log

# Create your views here.
NOTSET = 0
DEBUG = 10
INFO = 20
WARN = 30
ERROR = 40
CRITICAL = 50

columnCount = 4

def check_phonenumber(number:str)->bool:
    return re.match(r'\+375\(\d\d\)\d{7}', number)

def check_number(numb:str)->bool:
    return re.match(r"\d\d\d\d [A-Z][A-Z]-\d", numb) or \
            re.match(r"[A-Z][A-Z]-\d \d\d\d\d", numb) or \
            re.match(r"\d[A-Z][A-Z]T \d\d\d\d", numb)

def staffpage(func):
    def _(request):
        if not request.user.is_staff:
            return HttpResponseRedirect('main')
        return func(request)
    return _


def userpage(func):
    def _(request:HttpRequest):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")
        return func(request)
    return _

def index(request: HttpRequest):
    log.log(INFO, "somebody on the main page")
    if request.method == "GET":
        resp = get("https://official-joke-api.appspot.com/random_joke")
        joke = json.loads(resp.text)
        fact = json.loads(get("https://catfact.ninja/fact").text)['fact']

        return render(
            request,
            "index.html",
            {"setup": joke["setup"], "punchline": joke["punchline"], "fact":fact},
        )


# def login_in(request: HttpRequest):
#     form = LoginForm()
#     print(request.user.is_authenticated)
#     print(request.user.username)
#     print(request.method)
#     if request.method == 'POST':
#         print('Method is POST')
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except:
#             print('troubles no such user')
#             messages.error(request, "Такого пользователя не существует")
#         else:
#             print(f'there is user named {username}')
#         user = authenticate(request, username=username)
#         if user is not None:
#             print('try to login')
#             login(request, user)
#             return HttpResponseRedirect('user')
#         else:  
#             print('toubles wrong data')     
#             messages.error(
#                 request, 'Некорректный логин ИЛИ пароль. Проверьте введённые давнные.')
#     return render(request, "login.html", {'form':form})

@userpage
def logout_out(request:HttpRequest):
    logout(request)
    return HttpResponseRedirect('main')

@userpage
def order(request: HttpRequest):
    log.log(INFO, "somebody on the order page")

    if request.method == "GET":
        form = OrderForm()
        
        id = request.GET.get("id")
        if not AutoModel.objects.filter(carModel_id=id):
            return HttpResponseRedirect("catalog")
        return render(request, "order.html", {'form':form, 'id':id})
    elif request.method == "POST":
        print(request.POST)
        pst = request.POST
        ordr = OrderModel()
        now = datetime.datetime.now()
        beg = datetime.datetime.strptime(
            pst.get('dateTimeBegin'), "%Y-%m-%dT%H:%M")
        if beg < now:
            return HttpResponseRedirect(f"order?id={pst.get('id')}")
        
        end = datetime.datetime.strptime(
            pst.get('dateTimeEnd'), "%Y-%m-%dT%H:%M")
        if end - beg < datetime.timedelta(hours=1) or end < beg:
            return HttpResponseRedirect(f"order?id={pst.get('id')}")

        ordr.dateBegin = beg

        ordr.dateEnd = end
        ordr.dateEndFact = None
        clt = ClientModel.objects.get(user=request.user)
        ordr.client = clt
        auto = AutoModel.objects.filter(carModel__id=int(pst.get('id')), status=AutoModel.FREE).first()
        ordr.auto = auto
        ordr.save()
        
        auto.status = AutoModel.ON_ORDER
        auto.save()
        ordr.price = CarModel.objects.get(id=int(pst.get('id'))).price
        
        ordr.discounts.set(clt.discounts.all())
        ordr.count_price()
        ordr.save()

        return HttpResponseRedirect("user")
        


def catalog(request: HttpRequest):
    if request.method == "GET":
        lst = []
        tmp_list = list()
        i = 0
        for carModel in CarModel.objects.all():
            print(carModel)
            if i % columnCount == 0 and i != 0:
                lst.append(tmp_list)
                tmp_list = list()
            if AutoModel.objects.filter(status=AutoModel.FREE, carModel=carModel):
                tmp_list.append(carModel)
                i += 1

        if tmp_list:
            lst.append(tmp_list)
        print(lst)
        return render(request, "catalog.html", {"models": lst})


def redirect_index(request: HttpRequest):
    if request.method == "GET":
        return HttpResponseRedirect("main")

def registration(request: HttpRequest):
    form = RegistrationForm()
    if request.method == 'POST':
        pst = request.POST
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            if not check_phonenumber(pst.get('phone')):
                return render(request, "registration.html", {'form': form})
            if pst.get('password1') != pst.get('password2'):
                return render(request, "registration.html", {'form': form})

            usr = form.save(commit = False)
            client = ClientModel()
            client.f = pst.get('f')
            client.i = pst.get('i')
            client.o = pst.get('o')
            client.adress = pst.get('adress')
            client.phone = pst.get('phone')
            client.user = usr
            usr.save()
            client.save()
            log.log(INFO, "new client created")

            return HttpResponseRedirect('login')
        else:
            messages.error(request, 'Во время регистрации возникла ошибка')
    return render(request, "registration.html", {'form': form})

@staffpage
def searchuser(request:HttpRequest):
    log.log(INFO, "somebody enter the staff page")

    if request.method == "GET":
        return render(request, 'searchuser.html')
    if request.method == "POST":
        print(request.POST)
        if not check_phonenumber(request.POST.get('phone')):
            return render(request, "staff.html")
        f = request.POST.get('f')
        i = request.POST.get('i')
        o = request.POST.get('o')
        phone = request.POST.get('phone')[1::]

        return HttpResponseRedirect(f'userinfo?f={f}&i={i}&o={o}&phone={phone}')

@staffpage
def userinfo(request:HttpRequest):
    if request.method == "GET":
        f = request.GET.get('f')
        i = request.GET.get('i')
        o = request.GET.get('o')
        phone = '+' + request.GET.get('phone')
        log.log(DEBUG, f"phone {phone}")
        try:
            clt = ClientModel.objects.get(f=f, i=i, o=o, phone=phone)
        except ClientModel.DoesNotExist:
            log.log(DEBUG, f"not existing user {f} {i} {o} {phone}")
            return HttpResponseRedirect("searchuser")

        ordrs = OrderModel.objects.filter(client=clt)
        ordrsUnactive = ordrs.filter(isActive=False, dateEndFact=None)
        ordrsActive = ordrs.filter(isActive=True)
        discs = clt.discounts.all()
        pens = PenaltyModel.objects.all()
        return render(request, "userinfo.html", {'ordrsActive': ordrsActive, "ordrsUnactive": ordrsUnactive, 
                                                "client": clt, "discs": discs, "pens": pens, 'phone': request.GET.get('phone')})
    if request.method == 'POST':
        return stopOrder(request)
    
@staffpage
def stopOrder(request:HttpRequest):
    pst = request.POST
    f = pst.get('f')
    i = pst.get('i')
    o = pst.get('o')
    phone = pst.get('phone')
    # print(pst)
    ordr = OrderModel.objects.get(id=int(pst.get('id')))
    ordr.isActive = False

    ordr.dateEndFact = datetime.datetime.now()
    ordr.auto.status = AutoModel.FREE
    ordr.auto.usageCount += 1
    ordr.auto.carModel.usageCount += 1
    ordr.auto.carModel.save(update_fields=['usageCount'])
    ordr.auto.save(update_fields=["status", 'usageCount'])

    ps = list()
    ps_list = pst.get('penalties')
    if ps_list:
        for p in ps_list:
            ps.append(PenaltyModel.objects.get(id=int(p)))
        
        ordr.penalties.set(ps)
    

    ordr.count_price()
    print(ordr.price)

    # PenaltyModel.objects.get(id=)
    ordr.save(update_fields=['isActive', 'dateEndFact', 'price'])
    return HttpResponseRedirect(f"userinfo?f={f}&i={i}&o={o}&phone={phone}")

@userpage
def personal(request:HttpRequest):
    lst = list()
    clt = ClientModel.objects.get(user=request.user)
    try:
        lst += [str(p) for p in clt.discounts.all()]
    except:
        print('error in discounts')
    # try:
    #     lst += [str(d) for d in clt.penalties.all()]
    # except:
    #     print('error in penalties')
    
    ordrs = OrderModel.objects.filter(client__user=request.user)
    ordrsUnactive = ordrs.filter(isActive=False, dateEndFact=None)
    ordrsActive = ordrs.filter(isActive=True)

    return render(request, "user.html", {'d_p':lst, "ordrs":ordrsUnactive, "ordrsActive":ordrsActive})

@userpage
def cancel(request:HttpRequest):
    id = int(request.GET.get('id'))
    order = OrderModel.objects.get(id=id)
    order.auto.status = AutoModel.FREE
    order.auto.save(update_fields=["status"])

    order.auto.save()
    order.delete()
    return HttpResponseRedirect("user")

@staffpage
def activate(request:HttpRequest):
    if request.method == "GET":
        gt = request.GET
        f = gt.get('f')
        i = gt.get('i')
        o = gt.get('o')
        phone = gt.get('phone')
        # print(gt)
        ordr = OrderModel.objects.get(id=gt.get('id'))
        ordr.isActive = True
        ordr.save(update_fields=['isActive'])
        return HttpResponseRedirect(f"userinfo?f={f}&i={i}&o={o}&phone={phone}")

@staffpage
def cancelOrder(request:HttpRequest):
    if request.method == "GET":
        gt = request.GET
        f = gt.get('f')
        i = gt.get('i')
        o = gt.get('o')
        phone = gt.get('phone')
        # print(gt)
        ordr = OrderModel.objects.get(id=gt.get('id'))
        ordr.auto.status = AutoModel.FREE
        ordr.auto.save(update_fields=["status"])
        ordr.delete()
        return HttpResponseRedirect(f"userinfo?f={f}&i={i}&o={o}&phone={phone}")

@staffpage
def diagram(request:HttpRequest):
    models = CarModel.objects.all()
    models_names = [str(carModel) for carModel in models]
    usages = [carModel.usageCount for carModel in models]
    print('usages' + str(usages))
    print('models' + str(models_names))

    data = pltl.Bar(x=models_names, y=usages, marker=dict(color=['pink', 'gray', 'white']))
    layout = pltl.Layout(title='Статистика моделей по популярности',
                    xaxis=dict(title='модели'),
                    yaxis=dict(title='Общее количество заказов'))
    fig = pltl.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return render(
        request,
        'diagram.html',
        context={'plot_div': plot_div, }
    )

@staffpage
def statistics(request:HttpRequest):
    max_usage_carmodel = max(CarModel.objects.all(), key= lambda cm: cm.usageCount)
    max_usage_auto = max(AutoModel.objects.all(), key= lambda auto: auto.usageCount)
    max_user = max(ClientModel.objects.all(), key=lambda clt: len(OrderModel.objects.filter(client=clt)))
    staff_count = len(User.objects.filter(is_staff=True))   

    data = {'model':max_usage_carmodel, 'auto':max_usage_auto, 'usr':max_user, 'staff_count':staff_count}

    return render(request, 'statistics.html', data)
    
@staffpage
def addmodel(request:HttpRequest):
    fail = False
    if request.method == "POST":
        pst = request.POST

        year = int(pst.get('year'))
        if year >= 2010 and year <= datetime.datetime.now().year:
            mod = CarModel()
            mod.body = CarModel.BODY_CHOICES[int(pst.get('body'))][0]
            log.log(DEBUG, f"Adding auto model by brand {pst.get('brand')}")
            mod.brand = pst.get('brand')
            mod.car_price = int(pst.get('car_price'))
            mod.price = int(pst.get('price'))
            mod.year = int(pst.get('year'))
            mod.save()
        else:
            fail = True
    
    brands = [brand[0] for brand in CarModel.BRAND_CHOICES]
    bodies = [(i, body[1]) for i,body in enumerate(CarModel.BODY_CHOICES)]
    return render(request, "addmodel.html", {"brands":brands, "bodies":bodies, 'fail':fail})

@staffpage
def addauto(request:HttpRequest):
    fail = False
    if request.method == "POST":
        pst = request.POST
        if check_number(pst.get('number')):
            auto = AutoModel()
            auto.carModel = CarModel.objects.get(id=int(pst.get('auto')))
            auto.number = pst.get('number')
            auto.save()
        else:
            fail = True
        
    cars = CarModel.objects.all()
    return render(request, "addauto.html", {'cars':cars, 'fail':fail})

@staffpage
def staff(request):
    return render(request, "staff.html")

@staffpage
def delete(request:HttpRequest):
    if request.method == "GET":
        gt = request.GET
        id = int(gt.get('id'))
        if gt.get('model') == 'carmod':
            CarModel.objects.get(id=id).delete()
            return HttpResponseRedirect('modellist')
        elif gt.get('model') == 'auto':
            AutoModel.objects.get(id=id).delete()
            return HttpResponseRedirect('autolist')
    
    log.log(ERROR, "Tried to delete unknown model")
    return HttpResponseRedirect('main')

@staffpage
def editmodel(request:HttpRequest):
    fail = False
    id = 0
    if request.method == "POST":
        pst = request.POST
        year = int(pst.get('year'))
        if year >= 2010 and year <= datetime.datetime.now().year:
            id = int(pst.get('id'))
            mod = CarModel.objects.get(id=id)
            mod.body = CarModel.BODY_CHOICES[int(pst.get('body'))][0]
            log.log(DEBUG, f"Adding auto model by brand {pst.get('brand')}")
            mod.brand = pst.get('brand')
            mod.car_price = int(pst.get('car_price'))
            mod.price = int(pst.get('price'))
            mod.year = int(pst.get('year'))
            mod.save()
        else:
            fail = True
    else:
        id = int(request.GET.get('id'))
        mod = CarModel.objects.get(id=id)
    
    brands = [brand[0] for brand in CarModel.BRAND_CHOICES if brand[0] != mod.brand]
    bodies = [(i, body[1]) for i,body in enumerate(CarModel.BODY_CHOICES) if body[0] != mod.body]

    body = None
    for i, body_choice in enumerate(CarModel.BODY_CHOICES):
        if body_choice[0] == mod.body:
            body = (i, body_choice[1])
            break
    brand = mod.brand

    return render(request, "editmodel.html", 
                  {"brands":brands, "bodies":bodies, 'fail':fail, 'obj':mod, "body":body, "brand":brand, 'id':id})

@staffpage
def modellist(request:HttpRequest):
    if request.method == "GET":
        lst = []
        tmp_list = list()
        i = 0
        for carModel in CarModel.objects.all():
            print(carModel)
            if i % columnCount == 0 and i != 0:
                lst.append(tmp_list)
                tmp_list = list()
            tmp_list.append(carModel)
            i += 1

        if tmp_list:
            lst.append(tmp_list)
        print(lst)
        return render(request, "modellist.html", {"models": lst})
    
@staffpage
def autolist(request: HttpRequest):
    if request.method == "GET":
        lst = []
        tmp_list = list()
        i = 0
        for auto in AutoModel.objects.all():
            print(auto)
            if i % columnCount == 0 and i != 0:
                lst.append(tmp_list)
                tmp_list = list()
            tmp_list.append(auto)
            i += 1

        if tmp_list:
            lst.append(tmp_list)
        print(lst)
        return render(request, "autolist.html", {"autos": lst})

@staffpage
def editauto(request: HttpRequest):
    fail = False
    id = 0
    if request.method == "POST":
        pst = request.POST
        id = pst.get('id')
        auto = AutoModel.objects.get(id=id)
        if check_number(pst.get('number')):
            auto.carModel = CarModel.objects.get(id=int(pst.get('auto')))
            auto.number = pst.get('number')
            auto.save()
        else:
            fail = True
    else:
        id = int(request.GET.get('id'))
        auto = AutoModel.objects.get(id=id)
    cars = [mod for mod in CarModel.objects.all() if mod.id != id]
    car = auto.carModel
    return render(request, "editauto.html", {'cars':cars, 'fail':fail, "car":car, "obj":auto, "id":id})