from .cart import Cart


def cart(request):
    print("Cart context processor called")
    return {'cart': Cart(request)}
