from django.shortcuts import render

def home(request):
    return render(request, 'main.html')


def cart(request):
    return render(request, 'home/cart.html')

def checkout(request):
    return render(request, 'home/checkout.html')