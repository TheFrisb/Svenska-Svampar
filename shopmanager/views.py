from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from wkhtmltopdf.views import PDFTemplateResponse
from shop.models import Order, OrderItem, UserProfile, Product, UserClass, ProductPrice
from .models import *
from .mail_api import send_mails
from .pdf_generation import generate_pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
# Create your views here.


def shopmanager_home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            products = Product.objects.all().order_by('-created_at')
            organizations = UserProfile.objects.all().values('id', 'business_name')
            register_applications = Register_Application.objects.filter(is_dismissed=False).order_by('-created_at')
            new_registrations_count = register_applications.count()
            user_classes = UserClass.objects.all()
            new_user_profile_url = reverse('admin:shop_userprofile_add')
            # for all user_classes get the product name and their prices
            
            context = {
                'organizations': organizations,
                'products': products,
                'new_registrations_count': new_registrations_count,
                'user_classes': user_classes,
                'register_applications': register_applications,
                'title': 'Shop Manager Home',
                'new_user_profile_url': new_user_profile_url,

            }
            return render(request, 'shopmanager/shopmanager_home.html', context)
        else:
            return HttpResponse('You are not authorized to view this page')
    else:
        return HttpResponse('You are not authorized to view this page')


def shopmanager_view_orders(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        if(pk == 0):
            orders = Order.objects.prefetch_related('orderitem_set').order_by('-created_at')
        else:
            orders = Order.objects.prefetch_related('orderitem_set').filter(user_profile__id=pk).order_by('-created_at')
        organizations = UserProfile.objects.all().values('id', 'business_name')
        register_applications = Register_Application.objects.filter(is_dismissed=False).order_by('-created_at')
        new_registrations_count = register_applications.count()
        current_user = UserProfile.objects.filter(id=pk).values('id', 'business_name').first()

        paginator = Paginator(orders, 20)  # Show 10 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        context = {
            'orders': orders,
            'title': 'View Orders',
            'organizations': organizations,
            'new_registrations_count': new_registrations_count,
            'register_applications': register_applications,
            'title': 'Shopmanager Orders',
            'current_user': current_user,
            'page_obj': page_obj,
        }
        return render(request, 'shopmanager/view_orders.html', context)


def export_orders_as_pdf(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        order = Order.objects.prefetch_related('orderitem_set').filter(id=pk).first()
        organization = order.user_profile
        
        context = {
            'order': order,
            'organization': organization,
        }
        return PDFTemplateResponse(request, 'shopmanager/pdf_generation/view_order.html', context, cmd_options={'load-error-handling': 'ignore'})
    else:
        return HttpResponse('You are not authorized to view this page')



def register_applicant(request):
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        city = request.POST.get('city')
        contact_person = request.POST.get('contact_person')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        business_type = request.POST.get('business_type')
        registration_note = request.POST.get('registration_note', None)
        print(business_name, city, contact_person, phone_number, email, address, business_type, registration_note)
        if business_name and city and contact_person and phone_number and email and address and business_type:
            register_application = Register_Application.objects.create(
                business_name=business_name,
                city=city,
                contact_person=contact_person,
                phone_number=phone_number,
                email=email,
                address=address,
                business_type=business_type,
                registration_note=registration_note,
            )
            register_application.save()
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
    else:
        return HttpResponse('You are not authorized to view this page', status=401)
    

def dismiss_applicant(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff:
            try:
                applicant_id = request.POST.get('applicant_id')
                applicant = Register_Application.objects.get(id=applicant_id)
                applicant.is_dismissed = True
                applicant.save()
                return JsonResponse({'status': 'success', 'message': 'Applicant dismissed successfully'}, status=200)
            except:
                return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return HttpResponse('You are not authorized to view this page', status=401)