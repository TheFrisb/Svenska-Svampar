import base64
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
import logging
from shop.models import Order, Product
from shopmanager.models import Register_Application
from django.core.mail import EmailMessage
from decouple import config, Csv
logger = logging.getLogger('shopmanager')


def get_admin_url_for_object(obj):
    content_type = ContentType.objects.get_for_model(obj)
    admin_url = reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(obj.id,))
    return 'https://svenskasvampar.se' + admin_url


def format_email_html_content(title, html_content):
    valid_html = '''
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{title}</title>
                    <style>
                        /* Inline CSS styles for email compatibility */
                        body {{
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        }}
                    </style>
                    </head>
                <body>
                    <div>
                        {html_content}
                    </div>
                </body>
                </html>'''.format(title=title, html_content=html_content)
    return valid_html


def new_order_mail(order, pdf_path):
    return True
    title = f'[NEW ORDER] New Order from {order.user_profile.business_name} - {order.created_at.strftime("%d/%m/%Y %H:%M:%S")}'
    html_content = f'<p style="font-weight:600">The invoice is as an attachment</p>'
    valid_html = format_email_html_content(title, html_content)

    email = EmailMessage(
        subject=title,
        body=valid_html,
        to=config('ADMIN_EMAILS', cast=Csv()),
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
    return True
    if product.stock <= 50 and product.stock > 0:
        title = f'[LOW STOCK] Product {product.name} - {product.stock} left on stock'
        html_content = f'<p>Product <strong>{product.name}</strong> has <strong style="text-decoration:underline">{product.stock} stock left</strong></p><br>\
                      <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'
        valid_html = format_email_html_content(title, html_content)
        email = EmailMessage(
            subject=title,
            body=valid_html,
            to=config('ADMIN_EMAILS', cast=Csv()),
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
        title = f'[OUT OF STOCK] Product {product.name} - isout of stock'
        html_content =  html_content = f'<p>Product <strong>{product.name}</strong> is <strong style="text-decoration:underline">out of stock</strong></p><br>\
                            <a href="{get_admin_url_for_object(product)}" target="_blank" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Update stock</a>'
        valid_html = format_email_html_content(title, html_content)
        email = EmailMessage(
            subject=title,
            body=valid_html,
            to=config('ADMIN_EMAILS', cast=Csv()),
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
    return True
    link_url = 'https://svenskasvampar.se' + reverse('shopmanager:shopmanager-home')
    created_at_formatted = application.created_at.strftime('%Y-%m-%d %H:%M:%S')
    title = f'[INFO] New register application from {application.business_name}'
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
    valid_html = format_email_html_content(title, html_content)
    
    email = EmailMessage(
        subject=title,
        body=valid_html,
        to=config('ADMIN_EMAILS', cast=Csv()),
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
    return True
    business_name = user_profile.business_name
    title = f'[Failed order] Failed order from {business_name} - insufficient stock'
    html_content = f'<p>{business_name}, tried to order the following items, but they are out of stock:</p><br>'
    for item in email_insufficient_stock_items:
        html_content += f'<p><strong>{item["name"]}</strong> - x{item["quantity"]}, but we have only {item["stock_left"]} on stock</p>'
        html_content += f'<p>{business_name}</p>'
        html_content += f'<p>{user_profile.contact_person}</p><br>'
        html_content += f'<a href="tel:{user_profile.phone_number}" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Call {user_profile.phone_number}</a><br>'

    valid_html = format_email_html_content(title, html_content)
    

    email = EmailMessage(
        subject=title,
        body=valid_html,
        to=config('ADMIN_EMAILS', cast=Csv()),
    )
    email.content_subtype = "html"
    status = email.send()

    if status == 1:
        return True
    else:
        logger.exception(f'Error sending email for insufficient stock - {business_name}')
        return False
    

def failed_add_to_cart_mail(product, quantity, user_profile):
    return True
    business_name = user_profile.business_name
    title = f'[Failed add to cart] {business_name} tried to buy {product.name} - insufficient stock'
    html_content = f'<p>{business_name}, tried to add {product.name} x {quantity} to cart, but we only have {product.stock}</p>'
    html_content += f'<p>{user_profile.contact_person}</p><br>'
    html_content += f'<a href="tel:{user_profile.phone_number}" style="text-decoration: none;background: blue;font-weight: 600;padding: 5px 10px;border-radius: 4px;color: white;">Call {user_profile.phone_number}</a><br>'

    valid_html = format_email_html_content(title, html_content)

    email = EmailMessage(
        subject=title,
        body=valid_html,
        to=config('ADMIN_EMAILS', cast=Csv()),
    )
    email.content_subtype = "html"
    status = email.send()

    if status == 1:
        return True
    else:
        logger.exception(f'Error sending email for failed add to cart - {business_name}')
        return False
