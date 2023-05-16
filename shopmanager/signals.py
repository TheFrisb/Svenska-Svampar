from django.core import signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from shopmanager.mail_api import send_mails
from .models import Register_Application


@receiver(post_save, sender=Register_Application)
def product_quantity_mail(sender, instance, created, **kwargs):
    if created:
        print('Register application mail signal')
        send_mails.new_registerApplication_mail(instance)
