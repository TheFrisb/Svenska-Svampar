from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

from django.forms.models import BaseInlineFormSet

class ProductPriceInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # If UserClass is being created
            products = Product.objects.all()
            initial_data = [{'product': product} for product in products]
            self.initial = initial_data
            self.extra = len(products)



class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    formset = ProductPriceInlineFormSet
    extra = 0
    

class UserClassAdmin(admin.ModelAdmin):
    inlines = [ProductPriceInline]


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]


admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(UserClass, UserClassAdmin)
admin.site.register(Order, OrderAdmin)
