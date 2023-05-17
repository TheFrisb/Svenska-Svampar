import pdfkit
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.conf import settings
import os
from shop.models import Order, OrderItem, UserProfile, Product



def export_orders_as_pdf():
    organization = UserProfile.objects.filter().first()
    orders = Order.objects.prefetch_related('orderitem_set').filter().first()
    
    template = get_template('shopmanager/pdf_generation/view_order.html')
    context = {'organization': organization, 'orders': orders}
    html = template.render(context)

    
    output_filename = os.path.join(settings.MEDIA_ROOT, 'orders.pdf') # File path

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # wkhtmltopdf path
    pdfkit.from_string(html, output_filename, configuration=config)
    print('PDF generated at: ' + output_filename)
    return output_filename