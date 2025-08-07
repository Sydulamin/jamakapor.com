from django.shortcuts import render

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 1a2fe74802877d6e0e28ce48b891b158fc9cbf42
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