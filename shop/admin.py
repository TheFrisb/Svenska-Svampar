from django.contrib import admin
from .models import *
from django import forms
# Register your models here.
from django.forms.models import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html, mark_safe



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
    exclude = ('is_mail_sent', )
    def link(self, obj):
        if obj.id is not None:
            return format_html('<a href="{}" target="_blank">Export as PDF</a>', reverse('shopmanager:export-orders-as-pdf', args=[obj.id]))
        else:
            return 'New order, unable to export as PDF'
    
    link.allow_tags = True
    link.short_description = 'Export as PDF'
    @admin.display(description='User Profile', ordering='user_profile')
    def get_user_profile_with_order_id(self, obj):
        if obj.user is None:
            return f'Order: #{obj.id} - {obj.business_name} (Unregistered User)'
        else:
            return f'Order: #{obj.id} - {obj.user_profile}'

    list_display = ('get_user_profile_with_order_id', 'order_date', 'subtotal_price', 'total_price', 'invoice_number', 'invoice_ocr')
    inlines = [OrderItemsInline]

    fieldsets = (
        ('User Information', {
            'fields': ('user_profile', 'link'),
        }),
        ('Order Information', {
            'fields': ('subtotal_price', 'total_price', 'invoice_number', 'invoice_ocr')
        }),
        ('Unregistered User', {
            'classes': ('collapse',),
            'fields': ('business_name', 'organization_number', 'contact_person', 'city', 'address', 'postal_code')
        }),
    )
    readonly_fields = ['link']
    
    


    




class ProductAdmin(admin.ModelAdmin):
    exclude = ('mail_status', )
    list_display = ('name', 'stock','sku', 'ean_code', 'created_at', 'updated_at', )

    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'thumbnail', 'stock', 'quantity_shipped', 'sku', 'ean_code')
        }),
        ('Product details', {
            'fields': ('description', 'country_of_origin', 'temperature_storage', 'storage_information')
        }),
        ('Product nutrition (enter only a number)', {
            'fields': ('energy_kj', 'energy_kcal', 'fat', 'saturated_fat', 'monosaturated_fat', 'polyunsaturated_fat',
                        'carbohydrates', 'sugar', 'starch', 'protein', 'fiber', 'salt')
        }),

    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_class', 'created_at', 'updated_at',)



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserClass, UserClassAdmin)
admin.site.register(Order, OrderAdmin)
