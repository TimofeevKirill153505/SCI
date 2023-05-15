from django.db import models


class CarModel(models.Model):
    body = models.CharField(max_length=20)
    price = models.BigIntegerField(default=56, null=True)
    # car_price = models.BigIntegerField(default=56, null=True)
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=20)
    year = models.IntegerField()


class AutoModel(models.Model):
    id = models.AutoField(primary_key=True)
    carModel = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    number = models.CharField(max_length=10)
    status = models.CharField(max_length=20)


class DiscountModel(models.Model):
    id = models.AutoField(primary_key=True)
    percent = models.FloatField()
    name = models.CharField(max_length=30)


class PenaltyModel(models.Model):
    id = models.AutoField(primary_key=True)
    percent = models.FloatField()
    name = models.CharField(max_length=30)


class ClientModel(models.Model):
    id = models.AutoField(primary_key=True)
    f = models.CharField(max_length=30)
    i = models.CharField(max_length=30)
    o = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    adress = models.CharField(max_length=100)
    discounts = models.ManyToManyField(DiscountModel)
    penalties = models.ManyToManyField(PenaltyModel)


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    dateBegin = models.DateTimeField()
    dateEnd = models.DateTimeField()
    timeOfRent = models.TimeField()
    isActive = models.BooleanField()
    car = models.ForeignKey(AutoModel, on_delete=models.PROTECT)
    discounts = models.ManyToManyField(DiscountModel)
    penalties = models.ManyToManyField(PenaltyModel)
    price = models.IntegerField()
    client = models.ForeignKey(ClientModel, on_delete=models.PROTECT)
