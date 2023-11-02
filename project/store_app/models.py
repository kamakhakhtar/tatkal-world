from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

    
class SEO(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=200)
    # Add any other SEO-related fields here

    def __str__(self):
        return self.title


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Varient_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('10 TO 100','10 TO 100'),
        ('100 TO 500','100 TO 500'),
        ('500 TO 1000','500 TO 1000'),
        ('1000 TO 2000','1000 TO 2000'),
        ('2000 TO 3000','2000 TO 3000'),
        ('3000 TO 4000','3000 TO 4000')
        )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price

class Varient_test(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
       
class Product(models.Model):
    CONDITION = (
        ('NEW', 'NEW'),
        ('SALE', 'SALE'),
        ('TRENDING', 'TRENDING')
    )
    STOCK = (
        ('IN STOCK', 'IN STOCK'),
        ('OUT OF STOCK', 'OUT OF STOCK')
    )
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )
    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True)
    image = models.ImageField(upload_to="product_images/img")
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=50)
    description = models.TextField()
    stock = models.CharField(choices=STOCK, max_length=50)
    status = models.CharField(choices=STATUS, max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        total_price = 0  # Initialize total_price to 0

        # Check if there are variants associated with this product
        if self.varient_set.exists():
            # Get the first variant (you might want to handle multiple variants differently)
            variant = self.varient_set.first()
            total_price += variant.price

        # Set the calculated total price as the product price
        self.price = total_price

        if not self.unique_id:
            current_time = timezone.now()
            microseconds = current_time.strftime('%f')
            self.unique_id = current_time.strftime('%Y%m%d') + microseconds + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

              
class Images(models.Model):
    image = models.ImageField(upload_to="product_images/img")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Varient(models.Model):
    name = models.ForeignKey(Varient_Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    
    def __str__(self):
        return self.product.name
    


    
class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    message =  models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email        
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)    
    additional_info = models.TextField()
    product_info = models.TextField()
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=350, null=True, blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class OrderItem(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product  = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product_images/order_img")
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.Order.user.username
    
class Blog(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField('Categories')
    tags = models.ManyToManyField('Tag')
    images = models.ManyToManyField('Images', blank=True)
    status = models.CharField(choices=STATUS, max_length=50)

    def __str__(self):
        return self.title
    
class Carousel(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    page_link = models.CharField(max_length=200)  # URL for the call to action button
    discount_percentage = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Card(models.Model):
    image = models.ImageField(upload_to='card_images/')
    title = models.CharField(max_length=200)
    discount_percentage = models.PositiveIntegerField()
    call_to_action_link = models.CharField(max_length=200)  # URL for the call to action button

class IndexPage(models.Model):
    carousels = models.ManyToManyField('Carousel', related_name='index_page_carousels')
    cards = models.ManyToManyField('Card', related_name='index_page_cards')
    selected_products = models.ManyToManyField(Product, related_name='index_page_selected_products')
    selected_blogs = models.ManyToManyField(Blog, related_name='index_page_selected_blogs')

    def __str__(self):
        return "Index Page"
