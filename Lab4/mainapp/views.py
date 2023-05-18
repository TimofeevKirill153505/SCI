from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from requests import get
import django.http.request as req
from .models import CarModel, ClientModel, AutoModel
from .forms import RegistrationForm, LoginForm
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


def login_in(request: HttpRequest):
    form = LoginForm()
    print(request.user.is_authenticated)
    print(request.user.username)
    print(request.method)
    if request.method == 'POST':
        print('Method is POST')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print('troubles no such user')
            messages.error(request, "Такого пользователя не существует")
        else:
            print(f'there is user named {username}')
        user = authenticate(request, username=username)
        if user is not None:
            print('try to login')
            login(request, user)
            return HttpResponseRedirect('user')
        else:  
            print('toubles wrong data')     
            messages.error(
                request, 'Некорректный логин ИЛИ пароль. Проверьте введённые давнные.')
    return render(request, "login.html", {'form':form})

def logout_out(request:HttpRequest):
    logout(request)
    return HttpResponseRedirect('main')


def order(request: HttpRequest):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")

        return render(request, "order.html")
    elif request.method == "POST":
        pass
        


def catalog(request: HttpRequest):
    if request.method == "GET":
        lst = []
        tmp_list = list()
        i = 0
        for carModel in CarModel.objects.all():
            if i % columnCount == 0 and i != 0:
                lst.append(tmp_list)
                tmp_list = list()
            if carModel.automodel_set.get(status=AutoModel.FREE):
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
    return render(request, "user.html")