from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from requests import get
import django.http.request as req
from .models import CarModel

# Create your views here.

carModels = CarModel.objects.all()

if len(carModels) == 0:
    carModels = carModels.bulk_create(
        CarModel(body="седан", year=2013, price=110, brand="BMW"),
        CarModel(body="седан", year=2012, price=110, brand="BMW"),
        CarModel(body="седан", year=2011, price=110, brand="BMW"),
        CarModel(body="седан", year=2010, price=110, brand="BMW"),
        CarModel(body="седан", year=2009, price=110, brand="BMW"),
    )

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


def login(request: HttpRequest):
    if request.method == "GET":
        return render(request, "login.html")


def order(request: HttpRequest):
    if request.method == "GET":
        return render(request, "order.html")


def catalog(request: HttpRequest):
    if request.method == "GET":
        lst = []
        tmp_list = list()
        i = 0
        for carModel in carModels:
            if i % columnCount == 0 and i != 0:
                lst.append(tmp_list)
                tmp_list = list()
            tmp_list.append(carModel)
            i += 1

        if tmp_list:
            lst.append(tmp_list)
        print(lst)
        return render(request, "catalog.html", {"models": lst})


def redirect_index(request: HttpRequest):
    if request.method == "GET":
        return HttpResponseRedirect("main")
