from django.shortcuts import render

<<<<<<< HEAD
def home(request):
    return render(request, 'main.html')
=======
def store(request):
    return render(request, 'home/store.html')
>>>>>>> 8ac853f... Templates config


def cart(request):
    return render(request, 'home/cart.html')

def checkout(request):
    return render(request, 'home/checkout.html')