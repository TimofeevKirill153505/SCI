from django.db import models
from django.core.validators import  MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import re

def car_number_validator(numb:str)->bool:
    if re.match(r"\d\d\d\d [A-Z][A-Z]-\d", numb) or \
        re.match(r"[A-Z][A-Z]-\d \d\d\d\d", numb) or \
        re.match(r"\d[A-Z][A-Z]T \d\d\d\d", numb):
        return True
    else:
        raise ValidationError("Введенный номер не подходит ни под один разрешенный формат")

class CarModel(models.Model):
    SEDAN = "Седан"
    CROSS = "Кроссовер"
    COUPE = "Купе"
    STATION_WAGON = "Универсал"
    SPORT = "Спорт"
    HATCHBACK = "Хэтчбек"
    CONVERTIBLE = "Кабриолет"
    MINIVAN = "Минивэн"

    BODY_CHOICES = [
        (SEDAN, "Седан"),
        (CROSS, "Кроссовер"),
        (STATION_WAGON, "Универсал"),
        (SPORT, "Седан"),
        (HATCHBACK, "Хэтчбек"),
        (CONVERTIBLE, "Кабриолет"),
        (MINIVAN, "Минивэн"),
        (COUPE, "Купе"),

    ]

    BMW = "BMW"
    MERCEDES = "Mercedes"
    AUDI = "Audi"
    MAZDA = "Mazda"
    VOLVO = "Volvo"

    BRAND_CHOICES = [
        (BMW, 'BMW'),
        (MERCEDES, 'Mercedes'),
        (AUDI,"Audi"),
        (MAZDA, "Mazda"),
        (VOLVO, "Volvo")
    ]

    body = models.CharField(max_length=20, choices=BODY_CHOICES)
    price = models.BigIntegerField(default=40, null=True)
    car_price = models.BigIntegerField(default=10000, null=True)
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES)
    year = models.IntegerField(validators=[MaxValueValidator(2023), MinValueValidator(2010)])
    usageCount = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.brand} {self.body} {self.year}"


class AutoModel(models.Model):
    ON_ORDER = "На заказе"
    FREE = "Свободна"
    IN_REPAIR = "В ремонте"
    IN_SERVICE = "На обслуживании"
    STATUS_CHOICES = [
        (ON_ORDER, "На заказе"),
        (FREE, "Свободна"),
        (IN_REPAIR, "В ремонте"),
        (IN_SERVICE, "На обслуживании")
    ]
    id = models.AutoField(primary_key=True)
    carModel = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    number = models.CharField(max_length=9, validators=[car_number_validator])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    usageCount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.carModel.__str__()} {self.number}'


class DiscountModel(models.Model):
    id = models.AutoField(primary_key=True)
    percent = models.FloatField()
    name = models.CharField(max_length=30)
    usageCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PenaltyModel(models.Model):
    id = models.AutoField(primary_key=True)
    percent = models.FloatField()
    name = models.CharField(max_length=30)
    usageCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class ClientModel(models.Model):
    f = models.CharField(max_length=30)
    i = models.CharField(max_length=30)
    o = models.CharField(max_length=30)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15)
    adress = models.CharField(max_length=100)
    discounts = models.ManyToManyField(DiscountModel, null=True, default=None)
    # penalties = models.ManyToManyField(PenaltyModel, null=True, default=None)


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    dateBegin = models.DateTimeField()
    dateEnd = models.DateTimeField()
    dateEndFact = models.DateTimeField(null=True)
    isActive = models.BooleanField()
    car = models.ForeignKey(AutoModel, on_delete=models.PROTECT)
    discounts = models.ManyToManyField(DiscountModel)
    penalties = models.ManyToManyField(PenaltyModel)
    price = models.IntegerField()
    client = models.ForeignKey(ClientModel, on_delete=models.PROTECT)
