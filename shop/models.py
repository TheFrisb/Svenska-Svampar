from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
# Create your models here.





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Account', verbose_name='User')
    business_name = models.CharField(max_length=100, blank=True, unique=True, verbose_name='Business Name')
    organization_number = models.CharField(max_length=100, blank=True, unique=True, verbose_name='Organization Number', null=True)
    sweden_organization_number = models.CharField(max_length=100, blank=True, unique=True, verbose_name='Sweden Organization Number VAT NMMER', null=True)
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Contact Person')
    phone_number = models.CharField(max_length=100, blank=True, verbose_name='Phone Number')
    email = models.CharField(max_length=100, blank=True, verbose_name='Email')
    address = models.CharField(max_length=100, blank=True, verbose_name='Address')
    postal_code = models.CharField(max_length=100, blank=True, verbose_name='Postal Code')
    city = models.CharField(max_length=100, blank=True, verbose_name='City')
    user_class = models.ForeignKey('UserClass', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='User Class')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.business_name)
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Customers'
        verbose_name = 'Customer'



class Product(models.Model):
    name = models.CharField(max_length = 100, verbose_name='Name', db_index=True)
    stock = models.IntegerField(verbose_name='Stock')
    thumbnail = ProcessedImageField(upload_to='products/thumbnails/%Y/%m/%d/', processors=[ResizeToFill(550,550)], format='PNG', options={'quality': 100}, verbose_name='Thumbnail')
    quantity_shipped = models.FloatField(default=1, verbose_name='1 box contains in kg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mail_status = models.BooleanField(default=True)
    sku = models.CharField(max_length=100, blank=True, null=True, verbose_name='Article Number')
    ean_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='EAN Code')
    def __str__(self):
        return f'{self.name} - {self.stock} stock'
    
    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    
    @property
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=(self.id,))


class UserClass(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    products = models.ManyToManyField(Product, through='ProductPrice', verbose_name='Products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=(self.id,))
    
    
    class Meta:
        verbose_name_plural = 'User Classes'
        verbose_name = 'User Class'


class ProductPrice(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Product')
    price = models.FloatField(verbose_name='Price')
    user_class = models.ForeignKey(UserClass, on_delete=models.CASCADE, verbose_name='User Class')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Price for {self.product.name} by class {self.user_class.name}'
    
    class Meta:
        verbose_name_plural = 'Product Prices'
        verbose_name = 'Product Price'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User Profile')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Order Date')
    subtotal_price = models.FloatField(null = True, verbose_name='Subtotal Price (excl. VAT)')
    total_price = models.FloatField(null = True, verbose_name='Total Price')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    is_mail_sent = models.BooleanField(default=False, verbose_name='Is Mail Sent?')
    invoice_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='Invoice Number')
    invoice_ocr = models.CharField(max_length=100, blank=True, null=True, verbose_name='Invoice OCR')

    @property
    def get_order_vat(self):
        return self.total_price - self.subtotal_price

    @property
    def get_10_days_ahead(self):
        return self.order_date + timedelta(days=10)

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        ordering = ['-created_at']




    @property
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=(self.id,))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Quantity')
    price_each = models.FloatField(verbose_name='Price Each')
    total_price = models.FloatField(verbose_name='Total Price')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_quantity_in_kg(self):
        return self.product.quantity_shipped * self.quantity

    def __str__(self):
        if self.product is not None:
            return f'Order #{self.order.id} - {self.product.name}'
        else:
            return f'Order #{self.order.id} - Deleted Product'

    class Meta:
        verbose_name_plural = 'Order Items'
        verbose_name = 'Order Item'

