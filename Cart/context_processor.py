from.models import Cart,CartItem
from .views import _cart_id

#===it enough to get the cart count====#
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) # session key in _cart_id 
            cart_items = CartItem.objects.all().filter(cart=cart[:1])   # filter it a cart and we need one result
            for cart_item in cart_items:   
                cart_count += cart_item.quantity   # looping a cart items and increase the count of a product by home page
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)