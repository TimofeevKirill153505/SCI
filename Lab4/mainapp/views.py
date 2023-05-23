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

# Create your views here.

columnCount = 4


def index(request: HttpRequest):
    if request.method == "GET":
        resp = get("https://official-joke-api.appspot.com/random_joke")
        joke = json.loads(resp.text)
        return render(
            request,
            "index.html",
            {"setup": joke["setup"], "punchline": joke["punchline"]},
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

def logout_out(request:HttpRequest):
    logout(request)
    return HttpResponseRedirect('main')


def order(request: HttpRequest):
    if request.method == "GET":
        form = OrderForm()
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")
        id = request.GET.get("id")
        if not AutoModel.objects.filter(carModel_id=id):
            return HttpResponseRedirect("catalog")
        return render(request, "order.html", {'form':form, 'id':id})
    elif request.method == "POST":
        print(request.POST)
        pst = request.POST
        ordr = OrderModel()
        ordr.dateBegin = pst.get('dateTimeBegin')
        ordr.dateEnd = pst.get('dateTimeEnd')
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
            return HttpResponseRedirect('login')
        else:
            messages.error(request, 'Во время регистрации возникла ошибка')
    return render(request, "registration.html", {'form': form})

def stuff(request:HttpRequest):
    if request.method == "GET":
        return render(request, 'stuff.html')
    if request.method == "POST":
        print(request.POST)
        f = request.POST.get('f')
        i = request.POST.get('i')
        o = request.POST.get('o')
        phone = request.POST.get('phone')[1::]

        return HttpResponseRedirect(f'userinfo?f={f}&i={i}&o={o}&phone={phone}')
    
def userinfo(request:HttpRequest):
    if request.method == "GET":
        f = request.GET.get('f')
        i = request.GET.get('i')
        o = request.GET.get('o')
        phone = '+' + request.GET.get('phone')

        try:
            clt = ClientModel.objects.get(f=f, i=i, o=o, phone=phone)
        except ClientModel.DoesNotExist:
            return HttpResponseRedirect("stuff")

        ordrs = OrderModel.objects.filter(client=clt)
        ordrsUnactive = ordrs.filter(isActive=False, dateEndFact=None)
        ordrsActive = ordrs.filter(isActive=True)
        discs = clt.discounts.all()
        pens = PenaltyModel.objects.all()
        return render(request, "userinfo.html", {'ordrsActive': ordrsActive, "ordrsUnactive": ordrsUnactive, 
                                                "client": clt, "discs": discs, "pens": pens, 'phone': request.GET.get('phone')})
    if request.method == 'POST':
        return stopOrder(request)
    

def stopOrder(request:HttpRequest):
    pst = request.POST
    f = pst.get('f')
    i = pst.get('i')
    o = pst.get('o')
    phone = pst.get('phone')
    print(pst)
    ordr = OrderModel.objects.get(id=pst.get('id'))
    ordr.isActive = False

    ordr.dateEndFact = datetime.datetime.now()
    ordr.auto.status = AutoModel.FREE
    ordr.auto.usageCount += 1
    ordr.auto.carModel.usageCount += 1
    ordr.auto.carModel.save(['usageCount'])
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

def personal(request:HttpRequest):
    if request.user.is_staff:
        return HttpResponseRedirect("stuff")
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

def cancel(request:HttpRequest):
    id = int(request.GET.get('id'))
    order = OrderModel.objects.get(id=id)
    order.auto.status = AutoModel.FREE
    order.auto.save(update_fields=["status"])

    order.auto.save()
    order.delete()
    return HttpResponseRedirect("user")


def activate(request:HttpRequest):
    if request.method == "GET":
        gt = request.GET
        f = gt.get('f')
        i = gt.get('i')
        o = gt.get('o')
        phone = gt.get('phone')
        print(gt)
        ordr = OrderModel.objects.get(id=gt.get('id'))
        ordr.isActive = True
        ordr.save(update_fields=['isActive'])
        return HttpResponseRedirect(f"userinfo?f={f}&i={i}&o={o}&phone={phone}")

def cancelOrder(request:HttpRequest):
    if request.method == "GET":
        gt = request.GET
        f = gt.get('f')
        i = gt.get('i')
        o = gt.get('o')
        phone = gt.get('phone')
        print(gt)
        ordr = OrderModel.objects.get(id=gt.get('id'))
        ordr.auto.status = AutoModel.FREE
        ordr.auto.save(update_fields=["status"])
        ordr.delete()
        return HttpResponseRedirect(f"userinfo?f={f}&i={i}&o={o}&phone={phone}")
    
