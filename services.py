async def add_cart(name: str, quantity: int, items: dict, cart: dict):

    if cart:
        product = cart[name]
        if name in cart.keys():
            in_cart_qnt = int(cart[name]['quantity'])
            if quantity == 0:
                del product
            elif in_cart_qnt > quantity:
                product['quantity'] = quantity
            else:
                product['quantity'] = quantity
        else:
           cart.update(items)
    else:
        cart = dict()
        cart.update(items)