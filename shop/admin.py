from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

from django.forms.models import BaseInlineFormSet

class ProductPriceInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # If UserClass is being created
            products = Product.objects.all().order_by('name')
            initial_data = [{'product': product} for product in products]
            self.initial = initial_data
            self.extra = len(products)



class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    formset = ProductPriceInlineFormSet
    extra = 0
    # order by productprice.product.name
    ordering = ('product__name',)
    

class UserClassAdmin(admin.ModelAdmin):
    ordering = ('name',)
    inlines = [ProductPriceInline]
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            queryset = queryset.exclude(name='Admin')
            return queryset


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]




class ProductAdmin(admin.ModelAdmin):
    exclude = ('mail_status', )
    list_display = ('name', 'stock','sku', 'ean_code', 'created_at', 'updated_at', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_class', 'created_at', 'updated_at',)



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserClass, UserClassAdmin)
admin.site.register(Order, OrderAdmin)
