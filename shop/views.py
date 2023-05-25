import logging
from django.shortcuts import render
from django.http import JsonResponse
import json
from shop.models import *
from shopmanager.models import Register_Application
from django.contrib.auth import authenticate, login
from shopmanager.mail_api import send_mails
from random import randint
from shopmanager.mail_api import send_mails
from shopmanager.pdf_generation import generate_pdf


logger = logging.getLogger('shop')

def shop_home(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_class = user_profile.user_class
        products = Product.objects.all().order_by('name')
        product_prices = {}
        for product in products:
            try:
                price = ProductPrice.objects.get(product=product, user_class=user_class)
                product_prices[product] = price
            except ProductPrice.DoesNotExist:
                product_prices[product] = None


        context = {
            'user_profile': user_profile,
            'product_prices': product_prices,
        }
        if request.user.is_staff:
            context['is_admin'] = True
            context['new_registrations_count'] = Register_Application.objects.filter(is_dismissed=False).count()
    else:
        user_profile = None
        products = Product.objects.all()
        product_prices = {}
        for product in products:
            product_prices[product] = None
        context = {
            'user_profile': user_profile,
            'product_prices': product_prices,
        }

    return render(request, 'shop/shop_home.html', context=context)


def check_product_quantity(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            product_id = int(request.GET.get('product_id'))
            quantity = int(request.GET.get('quantity'))

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist.'}, status=400)
            
            if (quantity > product.stock):
                user_profile = UserProfile.objects.get(user=request.user)
                send_mails.failed_add_to_cart_mail(product, quantity, user_profile)
                return JsonResponse({'error': 'Not enough stock.'}, status=400)
            else:
                return JsonResponse({'message': 'Enough stock.'}, status=200)
            
        else:
            return JsonResponse({'error': 'Not authenticated.'}, status=400)
        
    else:
        return JsonResponse({'error': 'Wrong request method.'}, status=400)
    

def create_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_class = user_profile.user_class
            cart_items = json.loads(request.POST.get('cartItems'))
            if not cart_items:
                return JsonResponse({'error': 'Cart is empty.'}, status=400)
           # print(cart_items)
            insufficient_stock_items = []
            email_insufficient_stock_items = []
            for prod_id, quantity in cart_items.items():
                product_id = int(prod_id)
                quantity = int(quantity)
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return JsonResponse({'error': 'Product does not exist.'}, status=400)
                
                if quantity > product.stock and product.stock > 0:
                    insufficient_stock_items.append(product_id)
                    invalid_product_dict = {
                        'name': product.name,
                        'quantity': quantity,
                        'stock_left': product.stock,
                    }
                    email_insufficient_stock_items.append(invalid_product_dict)
                    
            
            if insufficient_stock_items:
                send_mails.insufficient_stock_mail(user_profile, email_insufficient_stock_items)
                return JsonResponse({
                    'error': 'Not enough stock for some items',
                    'insufficient_stock_items': insufficient_stock_items
                    }, status=400)
            else:
                order = Order.objects.create(user=user, user_profile = user_profile)
                order_subtotal = 0
                order_total = 0
                created_products = []
                for prod_id, quantity in cart_items.items():
                    product = Product.objects.get(id=int(prod_id))
                    product_price = ProductPrice.objects.filter(product=product, user_class=user_class).values_list('price', flat=True).get()
                    order_subtotal += product_price * quantity
                    OrderItem.objects.create(order=order, product=product, quantity=quantity,
                                              price_each = product_price, total_price = product_price * quantity)
                    product.stock -= quantity
                    product.save()
                    product_dict = {
                        'name': product.name,
                        'quantity': quantity,
                        'price': product_price,
                        'total_price': product_price * quantity,
                    }
                    created_products.append(product_dict)

                order_total = order_subtotal + (order_subtotal * 0.12)
                order.subtotal_price = order_subtotal
                order.total_price = order_total
                order.save()

                invoice_number = str(100 + order.id)
                invoice_ocr = invoice_number + str(randint(10, 99))

                Order.objects.filter(id=order.id).update(invoice_number=invoice_number, invoice_ocr=invoice_ocr)
                send_mails.new_order_mail(order, generate_pdf.export_orders_as_pdf(user_profile  ,order))
                return JsonResponse(
                    {
                    'message': 'Order created.',
                    'products': created_products,
                    'order_total': order_total,
                    }, status=200)
                
        else:
            return JsonResponse({'error': 'Not authenticated.'}, status=400)
        

def shop_login(request):
    if request.user.is_authenticated:
        return render(request, 'shop/shop_home.html')
    else:
        return render(request, 'shop/login.html')
    

def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'message': 'Login successful.'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=400)
    else:
        return JsonResponse({'error': 'Wrong request method.'}, status=400)
    




