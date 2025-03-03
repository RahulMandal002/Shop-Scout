from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.models import Product


def view_cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0

    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)

        # Remove non-numeric characters (e.g., currency symbols) from the price
        price = ''.join(filter(str.isdigit, product.price))  # Keeps only digits
        price = int(price)  # Convert to integer

        total += quantity * price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})

    return render(request, "cart.html", {'cart_items': cart_items, 'total': total, 'product_count': product_count})


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page.
    """

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0
    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})

    return {'cart_items': cart_items, 'total': total, 'product_count': product_count}


def add_to_cart(request, id):

    quantity=int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    print(cart)

    cart[id] = cart.get(id,quantity)
    #print(cart.get(id,quantity))
    request.session['cart'] = cart
    print(sum(request.session['cart'].values()))
    product_count = sum(request.session['cart'].values())

    context = {
        'product_count':product_count,
    }
    return redirect(reverse('index'))


def adjust_cart(request, id):
    quantity=int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    
    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)
        
    request.session['cart'] = cart    
    return redirect(reverse('view_cart'))