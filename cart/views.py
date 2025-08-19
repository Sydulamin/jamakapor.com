from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from product.models import Product 
# Create your views here.


def add_cart(request, id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:
        cart, created = request.user.cart_set.get_or_create(user = request.user,product=product)
        if not created:
            cart.quantity += 1
            cart.save()
    else:
        return redirect('login')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))