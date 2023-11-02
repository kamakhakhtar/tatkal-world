from django.contrib import admin

# Register your models here.
from .models import *

class ImagesTublerinLine(admin.TabularInline):
    model= Images

class TagTublerinLine(admin.TabularInline):
    model= Tag

class VarientTublerinLine(admin.TabularInline):
    model= Varient
    
class ProductAdmin(admin.ModelAdmin):
    inlines =[ImagesTublerinLine, TagTublerinLine, VarientTublerinLine]
    list_display = ('name', 'unique_id', 'price', 'condition', 'stock', 'status')

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines =[OrderItemTublerinline]


admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(ContactUs)


admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Filter_Price)
admin.site.register(Product, ProductAdmin)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Varient)
admin.site.register(Varient_Category)
admin.site.register(Varient_test)
admin.site.register(Blog)
admin.site.register(SEO)
admin.site.register(IndexPage)
