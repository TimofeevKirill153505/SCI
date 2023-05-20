from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from requests import get
import django.http.request as req
from .models import CarModel, ClientModel, AutoModel, OrderModel
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
        clt = ClientModel.objects.get(user=request.user)
        ordr.client = clt
        auto = AutoModel.objects.filter(carModel__id=int(pst.get('id')), status=AutoModel.FREE).first()
        ordr.auto = auto
        ordr.save()
        
        auto.status = AutoModel.ON_ORDER
        auto.save()
        ordr.price = CarModel.objects.get(id=int(pst.get('id'))).price
        
        ordr.discounts.set(clt.discounts.all())
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

def personal(request:HttpRequest):
    lst = list()
    clt = ClientModel.objects.get(user=request.user)
    try:
        lst += [str(p) for p in clt.discounts.all()]
    except:
        print('error in discounts')
    try:
        lst += [str(d) for d in clt.penalties.all()]
    except:
        print('error in penalties')
    
    ordrs = OrderModel.objects.filter(client__user=request.user)

    return render(request, "user.html", {'d_p':lst, "ordrs":ordrs})