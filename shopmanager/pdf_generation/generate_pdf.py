import pdfkit
from django.template.loader import get_template
from django.conf import settings
import os
from shop.models import Order
from decouple import config

WKHTMLTOPDF_PATH= config('WKHTMLTOPDF_PATH')

def export_orders_as_pdf(user_profile, order):

    order = Order.objects.prefetch_related('orderitem_set').filter(id=order.id).first()
    if order.user is not None:
        template = get_template('shopmanager/pdf_generation/delivery_note.html')
        context = {'organization': user_profile, 'order': order}
        html = template.render(context)

        
        output_filename = os.path.join(settings.PDF_ROOT, 'orders_' + str(order.id) + '.pdf') # File path

        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)  # wkhtmltopdf path
        pdfkit.from_string(html, output_filename, configuration=config)
        print('PDF generated at: ' + output_filename)
        return output_filename
    else:
        template = get_template('shopmanager/pdf_generation/delivery_note_unregistered.html')
        context = {'order': order}
        html = template.render(context)
        output_filename = os.path.join(settings.MEDIA_ROOT, 'orders.pdf') 
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH) 
        pdfkit.from_string(html, output_filename, configuration=config)
        print('PDF generated at: ' + output_filename)
        return output_filename
