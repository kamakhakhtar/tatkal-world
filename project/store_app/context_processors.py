
from store_app.models import Product, Categories
from cart.cart import Cart

def menu_items(request):
    categories = Categories.objects.all()
    products = Product.objects.all()
    grouped_menu = {}
    
    for category in categories:
        products_in_category = products.filter(categories=category)
        grouped_menu[category] = products_in_category
    
    cart = Cart(request)
    subtotal = sum(int(item['quantity']) * int(item['price']) for item in cart.cart.values())
    # random_products = Product.objecctts.filter(status='Publish').order_by('?')[:10]

    return {
        'grouped_menu': grouped_menu,
        'subtotal': subtotal,            
            }

    