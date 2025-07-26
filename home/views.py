from django.shortcuts import render

def store(request):
    return render(request, 'home/store.html')


def cart(request):
    return render(request, 'home/cart.html')

def checkout(request):
    return render(request, 'home/checkout.html')