from django.core import signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from shopmanager.mail_api import send_mails
from .models import Product, OrderItem, Order
from shopmanager.pdf_generation import generate_pdf
from shopmanager.mail_api import send_mails
from random import randint


@receiver(post_save, sender=Product)
def product_quantity_mail(sender, instance, created, **kwargs):
    if not created and instance.stock <= 50:
        print('Product quantity mail signal')
        mail_status = send_mails.product_quantity_mail(instance)
        

@receiver(post_save, sender=Order)
def send_new_order_mail(sender, instance, created, **kwargs):
    if created:
        instance.invoice_number = str(100 + instance.id)
        instance.invoice_ocr = instance.invoice_number + str(randint(10, 99))
        instance.save()
        
