from shop.models import Order
from shopmanager.mail_api import send_mails as sendgrid_send_mails
from shopmanager.pdf_generation import generate_pdf
from shopmanager.models import Register_Application
from shop.models import Product
import logging
from datetime import datetime

logger = logging.getLogger('cron')

def resend_unsent_mails():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'Cron job for resend_unsent_mails started at {date}')
    unsent_orderMails = Order.objects.filter(is_mail_sent=False)
    unsent_registerApplications = Register_Application.objects.filter(is_mail_sent=False)
    unsent_productStockUpdates = Product.objects.filter(mail_status=False)
    
    if unsent_orderMails:
        for order in unsent_orderMails:
            pdf_file_path = generate_pdf.export_orders_as_pdf()
            mail_status = sendgrid_send_mails.new_order_mail(order, pdf_file_path)
            if mail_status:
                logger.info(f'Order {order.id} - {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")} mail sent successfully')
            else:
                logger.error(f'Order {order.id} - {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")} mail not sent')


    if unsent_registerApplications:
        for application in unsent_registerApplications:
            mail_status = sendgrid_send_mails.new_registerApplication_mail(application)
            if mail_status:
                logger.info(f'RegisterApplication {application.id} - {application.business_name} - {application.created_at.strftime("%d/%m/%Y %H:%M:%S")} mail sent successfully')
            else:
                logger.error(f'RegisterApplication {application.id} - {application.business_name} - {application.created_at.strftime("%d/%m/%Y %H:%M:%S")} mail not sent')


    if unsent_productStockUpdates:
        for product in unsent_productStockUpdates:
            mail_status = sendgrid_send_mails.product_quantity_mail(product)
            if mail_status:
                logger.info(f'Product {product.id} - {product.name} - {product.stock} mail sent successfully')
            else:
                logger.error(f'Product {product.id} - {product.name} - {product.stock} mail not sent')
    

