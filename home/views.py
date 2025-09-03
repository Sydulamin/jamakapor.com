from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from product.models import Category, Product
from cart.models import Cart
from sslcommerz_lib import SSLCOMMERZ
from .models import Order
import uuid
import logging

logger = logging.getLogger(__name__)

# ---------- Home & Product Views ----------
def home(request):
    req_cat = request.GET.get('cat')
    products = Product.objects.filter(category__id=req_cat) if req_cat else Product.objects.all()
    cate = Category.objects.all()
    new_products = Product.objects.filter(new=True)
    context = {
        'cate': cate,
        'products': new_products,
        'all_products': products
    }
    return render(request, 'main.html', context)

def store(request):
    return render(request, 'home/store.html')

def cart(request):
    return render(request, 'home/cart.html')

def pro_details(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)
    product_quantity = 0
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, product=product).first()
        if cart_item:
            product_quantity = cart_item.quantity
    context = {'product': product, 'product_quantity': product_quantity}
    return render(request, 'home/product_D.html', context)

def checkout(request):
    return render(request, 'home/checkout.html')


# ---------- Payment Gateway ----------
def payment_gateway(request):
    # GET → show checkout summary
    if request.method != 'POST':
        cart_items = []
        total_amount = 0.0
        if request.user.is_authenticated:
            cart_qs = Cart.objects.filter(user=request.user)
            for c in cart_qs:
                cart_items.append(c)
                total_amount += float(getattr(c.product, 'price', 0)) * int(getattr(c, 'quantity', 1))
        else:
            session_cart = request.session.get('cart', {})
            for pid, qty in session_cart.items():
                try:
                    prod = Product.objects.get(id=pid)
                    prod.quantity = qty
                    prod.subtotal = float(getattr(prod, 'price', 0)) * int(qty)
                    cart_items.append(prod)
                    total_amount += prod.subtotal
                except Product.DoesNotExist:
                    continue
        return render(request, 'home/checkout.html', {'cart_items': cart_items, 'total_price': total_amount})

    # POST → create SSLCommerz session
    cart_items = []
    total_amount = 0.0
    num_of_item = 0
    product_names = []

    if request.user.is_authenticated:
        cart_qs = Cart.objects.filter(user=request.user)
        for c in cart_qs:
            price = float(getattr(c.product, 'price', 0)) or 0.0
            qty = int(getattr(c, 'quantity', 1)) or 1
            subtotal = price * qty
            total_amount += subtotal
            num_of_item += qty
            product_names.append(c.product.name)
            cart_items.append(c)
    else:
        session_cart = request.session.get('cart', {})
        for pid, qty in session_cart.items():
            try:
                prod = Product.objects.get(id=pid)
            except Product.DoesNotExist:
                continue
            price = float(getattr(prod, 'price', 0)) or 0.0
            qty = int(qty) or 1
            subtotal = price * qty
            total_amount += subtotal
            num_of_item += qty
            product_names.append(prod.name)
            prod.quantity = qty
            prod.subtotal = subtotal
            cart_items.append(prod)

    if total_amount <= 0:
        return render(request, 'home/cart.html', {'cart_items': cart_items, 'total_price': total_amount, 'error': 'Your cart is empty.'})

    # SSLCommerz setup
    settings = {'store_id': 'jamak68adae23ca437', 'store_pass': 'jamak68adae23ca437@ssl', 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)
    tran_id = str(uuid.uuid4())
    post_body = {
        'total_amount': round(total_amount, 2),
        'currency': "BDT",
        'tran_id': tran_id,
        'success_url': request.build_absolute_uri('/success/payment/'),
        'fail_url': request.build_absolute_uri('/fail/payment/'),
        'cancel_url': request.build_absolute_uri('/home/'),
        'emi_option': 0,
        'cus_name': request.user.get_full_name() if request.user.is_authenticated else request.POST.get('cus_name', 'Guest'),
        'cus_email': request.user.email if request.user.is_authenticated else request.POST.get('cus_email', 'guest@example.com'),
        'cus_phone': request.user.profile.phone if (request.user.is_authenticated and hasattr(request.user, 'profile') and getattr(request.user.profile, 'phone', None)) else request.POST.get('cus_phone', '01700000000'),
        'cus_add1': request.POST.get('cus_add1', 'customer address'),
        'cus_city': request.POST.get('cus_city', 'Dhaka'),
        'cus_country': request.POST.get('cus_country', 'Bangladesh'),
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': num_of_item,
        'product_name': ", ".join(product_names)[:250] if product_names else "Cart Items",
        'product_category': "General",
        'product_profile': "general"
    }

    # Save pending order with payment_info={} to satisfy NOT NULL constraint
    Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        guest_name=post_body['cus_name'] if not request.user.is_authenticated else None,
        guest_email=post_body['cus_email'] if not request.user.is_authenticated else None,
        tran_id=tran_id,
        status="Pending",
        amount=post_body['total_amount'],
        currency=post_body['currency'],
        payment_info={}  # <-- empty dict initially
    )

    response = sslcommez.createSession(post_body)
    if response.get('status') == 'SUCCESS':
        return HttpResponseRedirect(response['GatewayPageURL'])
    else:
        return render(request, 'home/checkout.html', {'error': 'Payment session failed. Please try again.'})


# ---------- Success & Fail ----------
@csrf_exempt
def success(request):
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
    logger.info("SSLCommerz success callback: %s", data)

    tran_id = data.get('tran_id')
    try:
        order = Order.objects.get(tran_id=tran_id)
        order.status = "Paid"  # or map SSLCommerz status to your own
        order.val_id = data.get('val_id')
        order.payment_info = data
        order.save()

        # ✅ Clear cart after successful payment
        if order.user:  # logged-in user
            Cart.objects.filter(user=order.user).delete()
        else:  # guest user
            request.session['cart'] = {}  # empty the session cart

    except Order.DoesNotExist:
        logger.error(f"No order found for tran_id {tran_id}")

    return render(request, 'home/success.html', {'payment': data})

def fail(request):
    return render(request, 'home/fail.html')
