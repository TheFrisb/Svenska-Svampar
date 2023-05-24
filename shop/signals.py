from django.core import signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from shopmanager.mail_api import send_mails
from .models import Product, OrderItem, Order
from shopmanager.pdf_generation import generate_pdf
from shopmanager.mail_api import send_mails


@receiver(post_save, sender=Product)
def product_quantity_mail(sender, instance, created, **kwargs):
    if not created and instance.stock <= 50:
        print('Product quantity mail signal')
        mail_status = send_mails.product_quantity_mail(instance)
        

# @receiver(post_save, sender=Order)
# def new_order_mailing(sender, instance, created, **kwargs):
#     if created:
#         pdf_path = generate_pdf.export_orders_as_pdf()
#         mail_status = send_mails.new_order_mail(instance, pdf_path)

