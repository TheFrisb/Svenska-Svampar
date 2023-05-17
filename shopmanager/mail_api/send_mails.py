from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import base64
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
import logging
import requests
from shop.models import Order, Product
from shopmanager.models import Register_Application


logger = logging.getLogger('shopmanager')


def get_admin_url_for_object(obj):
    content_type = ContentType.objects.get_for_model(obj)
    admin_url = reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(obj.id,))
    return 'http://127.0.0.1:8000' + admin_url


def new_order_mail(order, pdf_path):
    message = Mail(
            from_email='thefrisb@gmail.com',
            to_emails='bedzovski@yahoo.com',
            subject=f'New Order from {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")}',
            html_content = f'<p>Order invoice is as attachment</p><br>'
        )
    with open(pdf_path, 'rb') as f:
        data = f.read()
    encoded_file_data = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file_data),
        FileName(f'{order.user_profile.business_name}_{order.created_at.strftime("%d-%m-%Y")}.pdf'),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        Order.objects.filter(id=order.id).update(is_mail_sent=True)
        return True
    
    except Exception as e:
        logger.exception(f'Error sending email for order {order.id} - {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")} {str(e)}')
        Order.objects.filter(id=order.id).update(is_mail_sent=False)
        return False


def product_quantity_mail(product):
    if product.stock <= 50 and product.stock > 0:
        message = Mail(
            from_email='thefrisb@gmail.com',
            to_emails='bedzovski@yahoo.com',
            subject=f'[WARNING] Product {product.name} has {product.stock} stock left',
            html_content = f'<p>Product <strong>{product.name}</strong> has <strong style="text-decoration:underline">{product.stock} stock left</strong></p><br>\
                            <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'

        )
    elif product.stock == 0:
        message = Mail(
            from_email='thefrisb@gmail.com',
            to_emails='bedzovski@yahoo.com',
            subject=f'[OUT OF STOCK] Product {product.name} is out of stock!',
            html_content = f'<p>Product <strong>{product.name}</strong> is <strong style="text-decoration:underline">out of stock</strong></p><br>\
                            <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'

        )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        Product.objects.filter(id=product.id).update(mail_status=True)
        return True
        
    
    except Exception as e:
        logger.exception(f'Error sending email for stock update - {product.id} - {product.name} - {product.stock} {str(e)}')
        Product.objects.filter(id=product.id).update(mail_status=False)
        return False


def new_registerApplication_mail(application):
    link_url = 'http://127.0.0.1:8000' + reverse('shopmanager:shopmanager-home')
    created_at_formatted = application.created_at.strftime('%Y-%m-%d %H:%M:%S')
    message = Mail(
    from_email='thefrisb@gmail.com',
    to_emails='bedzovski@yahoo.com',
    subject=f'New register application from {application.business_name}',
    html_content = f'<p>New application ({created_at_formatted})</p> \
                    <p>Name: <strong>{application.business_name}</strong></p> \
                    <p>Contact person: <strong>{application.contact_person}</strong></p> \
                    <p>Phone: <strong>{application.phone_number}</strong></p> \
                    <p>Email: <strong>{application.email}</strong></p> \
                    <p>Address: <strong>{application.address}</strong></p> \
                    <p>City: <strong>{application.city}</strong></p><br> \
                    <a href="{link_url}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Check application</a>'
    )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        Register_Application.objects.filter(id=application.id).update(is_mail_sent=True)
        return True
    except Exception as e:
        logger.exception(f'Error sending email for new application - {application.id} - {application.business_name} - {application.created_at.strftime("%d/%m/%Y %H:%M:%S")} {str(e)}')
        Register_Application.objects.filter(id=application.id).update(is_mail_sent=False)
        return False
