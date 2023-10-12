from django.contrib import admin
from .models import CarModel, AutoModel, OrderModel, DiscountModel, PenaltyModel, ClientModel, NewsModel, ReviewModel
# Register your models here.

admin.site.register((CarModel, AutoModel, OrderModel,
                    DiscountModel, PenaltyModel, ClientModel, NewsModel, ReviewModel))
