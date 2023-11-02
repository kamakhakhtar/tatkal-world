from django import template
from store_app.models import Product

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return int(value) * int(arg)

@register.filter
def capitalize_first_letter(value):
    if value:
        return value.capitalize()
    return value

@register.filter
def product_slug(value):
    if value:
        parts = value.split("-")
        product = Product.objects.get(id=parts[0])
        
        return product.slug
    return value

