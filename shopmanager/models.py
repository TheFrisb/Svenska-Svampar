from django.db import models
from shop.models import Order, OrderItem
# Create your models here.


class Register_Application(models.Model):
    business_name = models.CharField(max_length=100, blank=True, verbose_name='Registrant Business Name')
    city = models.CharField(max_length=100, blank=True, verbose_name='Registrant City')
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Registrant Contact Person')
    phone_number = models.CharField(max_length=100, blank=True, verbose_name='Registrant Phone Number')
    email = models.CharField(max_length=100, blank=True, verbose_name='Registrant Email')
    address = models.CharField(max_length=100, blank=True, verbose_name='Registrant Address')
    business_type = models.CharField(max_length=100, blank=True, verbose_name='Registrant Business Type')
    registration_note = models.TextField(blank=True, verbose_name='Registrant Registration Note', null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Registrant Application Date')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Registrant Application Update Date')
    is_accepted = models.BooleanField(default=False, verbose_name='Registrant Application Acceptance Status')
    is_dismissed = models.BooleanField(default=False, verbose_name='Registrant Application Dismissal Status')
    is_mail_sent = models.BooleanField(default=False, verbose_name='Registrant Application Mail Sent Status')
    
    def __str__(self):
        return f'Application for: {self.business_name}'
    

    class Meta:
        verbose_name_plural = 'Registrant Applications'
        verbose_name = 'Registrant Application'