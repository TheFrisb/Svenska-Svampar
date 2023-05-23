#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import base64
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
import logging
from shop.models import Order, Product
from shopmanager.models import Register_Application
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
logger = logging.getLogger('shopmanager')


def get_admin_url_for_object(obj):
    content_type = ContentType.objects.get_for_model(obj)
    admin_url = reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(obj.id,))
    return 'https://svenskasvampar.se' + admin_url



# def new_order_mail(order, pdf_path):
#     message = Mail(
#             from_email='thefrisb@gmail.com',
#             to_emails='svenskasvampar@yahoo.com',
#             subject=f'New Order from {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")}',
#             html_content = f'<p>Order invoice is as attachment</p><br>'
#         )
#     with open(pdf_path, 'rb') as f:
#         data = f.read()
#     encoded_file_data = base64.b64encode(data).decode()

#     attachedFile = Attachment(
#         FileContent(encoded_file_data),
#         FileName(f'{order.user_profile.business_name}_{order.created_at.strftime("%d-%m-%Y")}.pdf'),
#         FileType('application/pdf'),
#         Disposition('attachment')
#     )
#     message.attachment = attachedFile

#     try:
#         sg = SendGridAPIClient(config('MAIL_SECRET_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#         Order.objects.filter(id=order.id).update(is_mail_sent=True)
#         return True
    
#     except Exception as e:
#         logger.exception(f'Error sending email for order {order.id} - {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")} {str(e)}')
#         Order.objects.filter(id=order.id).update(is_mail_sent=False)
#         return False




# def product_quantity_mail(product):
#     if product.stock <= 50 and product.stock > 0:
#         message = Mail(
#             from_email='thefrisb@gmail.com',
#             to_emails='svenskasvampar@yahoo.com',
#             subject=f'[WARNING] Product {product.name} has {product.stock} stock left',
#             html_content = f'<p>Product <strong>{product.name}</strong> has <strong style="text-decoration:underline">{product.stock} stock left</strong></p><br>\
#                             <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'

#         )
#     elif product.stock == 0:
#         message = Mail(
#             from_email='thefrisb@gmail.com',
#             to_emails='svenskasvampar@yahoo.com',
#             subject=f'[OUT OF STOCK] Product {product.name} is out of stock!',
#             html_content = f'<p>Product <strong>{product.name}</strong> is <strong style="text-decoration:underline">out of stock</strong></p><br>\
#                             <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'

#         )
#     try:
#         sg = SendGridAPIClient(config('MAIL_SECRET_KEY'))
#         response = sg.send(message)
#         Product.objects.filter(id=product.id).update(mail_status=True)
#         return True
        
    
#     except Exception as e:
#         logger.exception(f'Error sending email for stock update - {product.id} - {product.name} - {product.stock} {str(e)}')
#         Product.objects.filter(id=product.id).update(mail_status=False)
#         return False


# def new_registerApplication_mail(application):
#     link_url = 'http://127.0.0.1:8000' + reverse('shopmanager:shopmanager-home')
#     created_at_formatted = application.created_at.strftime('%Y-%m-%d %H:%M:%S')
#     message = Mail(
#     from_email='thefrisb@gmail.com',
#     to_emails='svenskasvampar@yahoo.com',
#     subject=f'New register application from {application.business_name}',
#     html_content = f'<p>New application ({created_at_formatted})</p> \
#                     <p>Name: <strong>{application.business_name}</strong></p> \
#                     <p>Contact person: <strong>{application.contact_person}</strong></p> \
#                     <p>Phone: <strong>{application.phone_number}</strong></p> \
#                     <p>Email: <strong>{application.email}</strong></p> \
#                     <p>Address: <strong>{application.address}</strong></p> \
#                     <p>City: <strong>{application.city}</strong></p><br> \
#                     <p>Business type: <strong>{application.business_type}</strong></p><br> \
#                     <p>Customer_note: <strong>{application.registration_note}</strong></p><br> \
#                     <a href="{link_url}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Check application</a>'
#     )
#     try:
#         sg = SendGridAPIClient(config('MAIL_SECRET_KEY'))
#         response = sg.send(message)
#         Register_Application.objects.filter(id=application.id).update(is_mail_sent=True)
#         return True
#     except Exception as e:
#         logger.exception(f'Error sending email for new application - {application.id} - {application.business_name} - {application.created_at.strftime("%d/%m/%Y %H:%M:%S")} {str(e)}')
#         Register_Application.objects.filter(id=application.id).update(is_mail_sent=False)
#         return False
    


# def insufficient_stock_mail(user_profile, email_insufficient_stock_items):
#     business_name = user_profile.business_name
#     html_content = f'<p>{business_name}, tried to order the following items, but they are out of stock:</p><br>'
#     for item in email_insufficient_stock_items:
#         html_content += f'<p><strong>{item["name"]}</strong> - x{item["quantity"]}, but we have only {item["stock_left"]} on stock</p><br>'
#         html_content += f'<p>{user_profile.contact_person}</p><br>'
#         html_content += f'<a href="tel:{user_profile.phone_number}" class="style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">{user_profile.phone_number}</a><br>'

#     message = Mail(
#         from_email='thefrisb@gmail.com',
#         to_emails='svenskasvampar@yahoo.com',
#         subject=f'[INFO] Failed order from {business_name} - insufficient stock',
#         html_content = html_content
#     )
    
#     try:
#         sg = SendGridAPIClient(config('MAIL_SECRET_KEY'))
#         response = sg.send(message)
#         return True
#     except Exception as e:
#         logger.exception(f'Error sending email for insufficient stock - {user_profile.id} - {user_profile.business_name} - {user_profile.created_at.strftime("%d/%m/%Y %H:%M:%S")} {str(e)}')
#         return False
    


def new_order_mail(order, pdf_path):
    html_content = f'<p style="font-weight:600">The invoice is as an attachment</p>'
    email = EmailMessage(
        subject=f'[NEW ORDER] New Order from {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")}',
        body=html_content,
        to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se'],
        attachments=[(f'order_{order.id}.pdf', open(pdf_path, 'rb').read(), 'application/pdf')],
    )
    email.content_subtype = "html"
    status = email.send()
    if status == 1:
        Order.objects.filter(id=order.id).update(is_mail_sent=True)
        return True
    else:
        logger.exception(f'Error sending email for new order - {order.id} - {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")}')
        Order.objects.filter(id=order.id).update(is_mail_sent=False)
        return False


def product_quantity_mail(product):
    if product.stock <= 50 and product.stock > 0:
        html_content = f'<p>Product <strong>{product.name}</strong> has <strong style="text-decoration:underline">{product.stock} stock left</strong></p><br>\
                      <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'
        email = EmailMessage(
            subject=f'[LOW STOCK] Product {product.name} - {product.stock} left on stock',
            body=html_content,
            to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se']
        )
        email.content_subtype = "html"
        status = email.send()
        if status == 1:
            Product.objects.filter(id=product.id).update(mail_status=True)
            return True
        else:
            logger.exception(f'Error sending email for low stock - {product.id} - {product.name}')
            Product.objects.filter(id=product.id).update(mail_status=False)
            return False
        
    elif product.stock == 0:
        html_content =  html_content = f'<p>Product <strong>{product.name}</strong> is <strong style="text-decoration:underline">out of stock</strong></p><br>\
                            <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'
        email = EmailMessage(
            subject=f'[OUT OF STOCK] Product {product.name} - isout of stock',
            body=html_content,
            to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se']
        )
        email.content_subtype = "html"  
        status = email.send()
        if status == 1:
            Product.objects.filter(id=product.id).update(mail_status=True)
            return True
        else:
            logger.exception(f'Error sending out of stock email for product {product.id} - {product.name}')
            Product.objects.filter(id=product.id).update(mail_status=False)
            return False
        


def new_registerApplication_mail(application):
    link_url = 'https://svenskasvampar.se' + reverse('shopmanager:shopmanager-home')
    created_at_formatted = application.created_at.strftime('%Y-%m-%d %H:%M:%S')
    html_content = f'<p>New application ({created_at_formatted})</p> \
                <p>Name: <strong>{application.business_name}</strong></p> \
                <p>Contact person: <strong>{application.contact_person}</strong></p> \
                <p>Phone: <strong>{application.phone_number}</strong></p> \
                <p>Email: <strong>{application.email}</strong></p> \
                <p>Address: <strong>{application.address}</strong></p> \
                <p>City: <strong>{application.city}</strong></p> \
                <p>Business type: <strong>{application.business_type}</strong></p> \
                <p>Customer note: <strong>{application.registration_note}</strong></p><br> \
                <a href="{link_url}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Check application</a>'
    
    email = EmailMessage(
        subject=f'[INFO] New register application from {application.business_name}',
        body=html_content,
        to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se']
    )
    email.content_subtype = "html"
    status = email.send()

    if status == 1:
        Register_Application.objects.filter(id=application.id).update(is_mail_sent=True)
        return True
    else:
        logger.exception(f'Error sending email for new application - {application.id} - {application.business_name} - {application.created_at.strftime("%d/%m/%Y %H:%M:%S")}')
        Register_Application.objects.filter(id=application.id).update(is_mail_sent=False)
        return False



def insufficient_stock_mail(user_profile, email_insufficient_stock_items):
    business_name = user_profile.business_name
    html_content = f'<p>{business_name}, tried to order the following items, but they are out of stock:</p><br>'
    for item in email_insufficient_stock_items:
        html_content += f'<p><strong>{item["name"]}</strong> - x{item["quantity"]}, but we have only {item["stock_left"]} on stock</p>'
        html_content += f'<p>{business_name}</p>'
        html_content += f'<p>{user_profile.contact_person}</p><br>'
        html_content += f'<a href="tel:{user_profile.phone_number}" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Call {user_profile.phone_number}</a><br>'

    email = EmailMessage(
        subject=f'[Failed order] Failed order from {business_name} - insufficient stock',
        body=html_content,
        to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se']
    )
    email.content_subtype = "html"
    status = email.send()

    if status == 1:
        return True
    else:
        logger.exception(f'Error sending email for insufficient stock - {business_name}')
        return False
    

def failed_add_to_cart_mail(product, quantity, user_profile):
    business_name = user_profile.business_name
    html_content = f'<p>{business_name}, tried to add {product.name} x {quantity} to cart, but we only have {product.stock}</p>'
    html_content += f'<p>{user_profile.contact_person}</p><br>'
    html_content += f'<a href="tel:{user_profile.phone_number}" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Call {user_profile.phone_number}</a><br>'

    email = EmailMessage(
        subject=f'[Failed add to cart] {business_name} tried to buy {product.name} - insufficient stock',
        body=html_content,
        to=['bedzovski@yahoo.com', 'thefrisb@gmail.com', 'info@svenskasvampar.se']
    )
    email.content_subtype = "html"
    status = email.send()

    if status == 1:
        return True
    else:
        logger.exception(f'Error sending email for failed add to cart - {business_name}')
        return False
