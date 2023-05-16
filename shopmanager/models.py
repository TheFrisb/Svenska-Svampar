from django.db import models
from shop.models import Order, OrderItem
# Create your models here.


class Register_Application(models.Model):
    business_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    is_mail_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Registered applicant with business name: {self.business_name}'
    

    class Meta:
        verbose_name_plural = 'Registrant Applications'
        verbose_name = 'Registrant Application'