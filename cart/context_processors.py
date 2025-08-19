from cart.models import Cart

def cart_context_processor(request):
    """
    Context processor to add cart information to the context.
    """
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_length = len(Cart.objects.filter(user=request.user))
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        print(f"Cart items: {cart_items}, Length: {cart_length}, Total Quantity: {total_quantity}, Total Price: {total_price}")
    else:
        cart_items = []
        total_quantity = 0
        total_price = 0

    return {
        'cart_items': cart_items,
        'cart_length': cart_length,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }