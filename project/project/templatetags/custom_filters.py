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
    value = str(value)  # Convert value to string

    if "-" in value:
        parts = value.split("-")
        product = Product.objects.get(id=parts[0])
        return product.slug
    else:
        product = Product.objects.get(id=value)
        return product.slug

@register.filter
def variant_price(id,price):
    value = str(value)  # Convert value to string

    if "-" in value:
        parts = value.split("-")
        product = Product.objects.get(id=parts[0])
        return product.slug
    else:
        product = Product.objects.get(id=value)
        return product.slug

