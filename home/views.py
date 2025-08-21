from django.shortcuts import render
from product.models import Category, Product
from cart.models import Cart

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

def checkout(request):
    return render(request, 'home/checkout.html')

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
