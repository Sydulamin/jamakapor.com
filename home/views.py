from django.shortcuts import render
from product.models import Category, Product
from cart.models import Cart
from sslcommerz_lib import SSLCOMMERZ
from django.http import HttpResponseRedirect
from django.urls import reverse
import uuid
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def home(request):
    req_cat = request.GET.get('cat')
    if req_cat:
        products = Product.objects.filter(category__id=req_cat)
    else:
        products = Product.objects.all()
    
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

@csrf_exempt
def success(request):
    """
    SSLCommerz will redirect here after successful payment.
    Collect all data sent by the gateway (GET or POST), log it,
    and pass it to the template. Validate/verify with the gateway
    server if you need extra security (not shown here).
    """
    # SSLCommerz may send params via GET or POST depending on config
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()

    # Common fields returned by SSLCommerz
    payment_info = {
        'status': data.get('status'),
        'tran_id': data.get('tran_id'),
        'val_id': data.get('val_id'),
        'amount': data.get('amount'),
        'currency': data.get('currency'),
        'bank_tran_id': data.get('bank_tran_id'),
        'card_type': data.get('card_type'),
        'card_issuer': data.get('card_issuer'),
        'card_brand': data.get('card_brand'),
        'card_issuer_country': data.get('card_issuer_country'),
        'store_amount': data.get('store_amount'),
        'verify_sign': data.get('verify_sign'),
        # include all received keys so template can inspect them
        'all_params': data,
    }

    # log for debugging / record keeping
    logger.info("SSLCommerz success callback received: %s", payment_info)
    print(payment_info)

    # TODO: verify val_id / verify_sign with SSLCommerz API if required,
    # record order in DB, update inventory, clear cart, send receipt email, etc.

    return render(request, 'home/success.html', {'payment': payment_info})

def fail(request):
    return render(request, 'home/fail.html')

def checkout(request):
    
    # collect cart data (for authenticated users). Adjust if you use session-based cart.
    return render(request, 'home/checkout.html')

def payment_gateway(request):
    # require POST from checkout form
    if request.method != 'POST':
        # compute cart summary to show on checkout page
        cart_items = []
        total_amount = 0.0
        if request.user.is_authenticated:
            cart_qs = Cart.objects.filter(user=request.user)
            for c in cart_qs:
                cart_items.append(c)
                total_amount += float(getattr(c.product, 'price', 0)) * int(getattr(c, 'quantity', 1))
        else:
            # session cart format: { product_id: quantity, ... }
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
        return render(request, 'home/checkout.html', {
            'cart_items': cart_items,
            'total_price': total_amount
        })

    # POST handling - gather cart and build SSLCommerz payload
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
        # read session cart for guests
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
            # create lightweight object for template/payload
            prod.quantity = qty
            prod.subtotal = subtotal
            cart_items.append(prod)

    if total_amount <= 0:
        return render(request, 'home/cart.html', {
            'cart_items': cart_items,
            'total_price': total_amount,
            'error': 'Your cart is empty.'
        })

    settings = { 'store_id': 'jamak68adae23ca437', 'store_pass': 'jamak68adae23ca437@ssl', 'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = round(total_amount, 2)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = str(uuid.uuid4())
    post_body['success_url'] = request.build_absolute_uri('/success/payment/')
    post_body['fail_url'] = request.build_absolute_uri('/fail/payment/')
    post_body['cancel_url'] = request.build_absolute_uri('/home/')
    post_body['emi_option'] = 0

    # prefer POST fields from checkout form for guest checkout
    post_body['cus_name'] = request.user.get_full_name() if request.user.is_authenticated else request.POST.get('cus_name', 'Guest')
    post_body['cus_email'] = request.user.email if request.user.is_authenticated else request.POST.get('cus_email', 'guest@example.com')
    post_body['cus_phone'] = request.user.profile.phone if (request.user.is_authenticated and hasattr(request.user, 'profile') and getattr(request.user.profile, 'phone', None)) else request.POST.get('cus_phone', '01700000000')
    post_body['cus_add1'] = request.POST.get('cus_add1', 'customer address')
    post_body['cus_city'] = request.POST.get('cus_city', 'Dhaka')
    post_body['cus_country'] = request.POST.get('cus_country', 'Bangladesh')
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_of_item
    names = ", ".join(product_names)[:250] if product_names else "Cart Items"
    post_body['product_name'] = names
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcommez.createSession(post_body)

    if response.get('status') == 'SUCCESS':
        return HttpResponseRedirect(response['GatewayPageURL'])
    else:
        return render(request, 'home/checkout.html', {'error': 'Payment session failed. Please try again.'})
    

def pro_details(request):
    product_id = request.GET.get('id')
    
    product = Product.objects.get(id=product_id)
    
    product_quantity=0
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        product_quantity = cart_item.quantity


    context = {
        'product': product,
        'product_quantity':product_quantity
    }
    return render(request, 'home/product_D.html', context)
