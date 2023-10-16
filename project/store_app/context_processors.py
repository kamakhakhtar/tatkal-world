
from store_app.models import Product, Categories

def menu_items(request):
    categories = Categories.objects.all()
    products = Product.objects.all()
    grouped_menu = {}
    
    for category in categories:
        products_in_category = products.filter(categories=category)
        grouped_menu[category] = products_in_category
    
    return {'grouped_menu': grouped_menu}