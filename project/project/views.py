# ========= DJANGO ===========
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from store_app.models import Product, Categories, Brand, ContactUs, Order, OrderItem, Varient

# cart
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.http import JsonResponse
from django.urls import reverse
import requests

from datetime import datetime

# ======== Alert Sound =======
# from playsound import playsound
# import pygame

# ========= MONGO DB =========
from pymongo import MongoClient

# ==== Variable Values ====

# Connect to MongoDB
uri = "mongodb+srv://tempsmsadmin:m0W1Rirs6pKJ1eri@cluster0.hfly6u2.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# client = MongoClient('mongodb://root:007arshad@localhost:27017/?authMechanism=DEFAULT')
# client = MongoClient('mongodb+srv://tempsmsadmin:m0W1Rirs6pKJ1eri@cluster0.hfly6u2.mongodb.net/')

# Access the database and collection
db = client['tempsms']
number_collection = db['numbers']
log_collection = db['logs']
temp_number_collection =db['tempnumber']


# ==================================
# =========== VIEWS ================
# ==================================

# ========== Login View ======================
def main_page(request):
     product = Product.objects.filter(status='Publish')
    
     context = {
          'product':product,
     }
     return render(request, 'index.html', context)

def product(request):
    product = Product.objects.filter(status='Publish')
    categories = Categories.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    SORT = request.GET.get('sort')
    if CATID:
         product = Product.objects.filter(categories = CATID)
    elif SORT:
        if SORT == "Price: low to high":
            product = Product.objects.filter(status = 'Publish').order_by('price')
        elif SORT == "Price: high to low" :     
            product = Product.objects.filter(status = 'Publish').order_by('-price')             
        else:
             product = Product.objects.filter(status = 'Publish', condition = SORT)
    else:
         product = Product.objects.filter(status = 'Publish')

    context = {
          'product':product,
          'categories':categories,
          'brand':brand,
     }
  
    return render(request, 'product.html',context)

def search(request):
    
    query = request.GET.get('query')    
    product = Product.objects.filter(name__contains = query, status = 'Publish' )
    
    context = {
          'product':product,
        'query':query,
     }
    return render(request, 'search.html',context)

def single_product(request, uid):
    product = Product.objects.filter(slug=uid).first()
    variant_price = 0
    if request.method == 'GET':    
     variant_name = request.GET.get('variant')  # Use 'variant' instead of 'variant_name'
     # Check if variant_name is provided in GET data
     if variant_name:
          # Get the variant price based on the variant name
          variant = product.varient_set.filter(name__name=variant_name).first()
          if variant:
               variant_price = variant.price
               #   print(variant_price)
               # Calculate total price by adding base price and variant price
               total_price = product.price + variant_price
               #   print(total_price)
     else:
          # If no variant is selected, the total price is just the base price
          total_price = product.price

    context = {
        'prod': product,
        'total_price': total_price
    }
    return render(request, 'single-product.html', context)


def shopping_cart(request):
     return render(request, 'cart.html')

def checkout(request):
     return render(request, 'checkout.html')

def about_us(request):
     return render(request, 'about-us.html')

def contact_us(request):
     if request.method == 'POST':
          name = request.POST.get('name')
          email = request.POST.get('email')
          phone = request.POST.get('phone')
          message = request.POST.get('message')
          
          contact = ContactUs(
               name = name,
               email = email,
               phone = phone,
               message = message
          )
          contact.save()
          return redirect('main')

     return render(request, 'contact-us.html')

def register(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          email = request.POST.get('email')
          pass1 = request.POST.get('pass1')
          pass2 = request.POST.get('pass2')

          customer = User.objects.create_user(username, email, pass1)
          customer.first_name = first_name
          customer.last_name = last_name
          customer.save()
          return render(request, 'index.html')

     return render(request, 'register.html')

def Handellogin(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          user = authenticate(username = username, password = password)
          if user is not None:
               login(request, user)
               return redirect('main')
          else:
               return redirect('login')
                    
     return render(request, 'login.html')


# def loginModal(request):
#      if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             response_data = {'success': True, 'username': user.get_full_name().title()}
#         else:
#             response_data = {'success': False, 'error_message': 'Bad credentials'}
            
#      return JsonResponse(response_data)
    
def HandelLogout(request):
     logout(request)     
     return render(request, 'login.html')
     # return JsonResponse({'success':True})

def privacy_policy(request):
     return render(request, 'privacy-policy.html')


def terms_conditions(request):
     return render(request, 'terms-conditions.html')

def blog_single(request):
     return render(request, 'blog-single.html')

def blogs(request):
     return render(request, 'blogs.html')

# @login_required(login_url="/login/")
def cart_add(request, id, variant):
    
     cart = Cart(request)     
     product = Product.objects.get(id=id)
     
     if variant != 'null':
          id = id + "-"+ variant
          p_name = f"{product.name} {variant} PNR"

          print("id :" + id )
          print("variant :" + variant)
          
          variant = product.varient_set.filter(name__name=variant).first()
          if variant:
               # Update the product price with the variant price
               product.price = variant.price + product.price
               product.id = id
               product.name = p_name     

     cart.add(product=product)
     items = len(cart.cart)
     total_subtotal = sum(int(item['quantity']) * int(item['price']) for item in cart.cart.values())
     return JsonResponse({
          'success': True,
          'item': items,
          # 'variant': variant_name,
          'total_subtotal': total_subtotal,  # Include total_subtotal in the response
          })


# @login_required(login_url="/login/")
def item_clear(request, id):

     # Split the slug into parts based on '-'
     parts = id.split('-')
     variant='null'
     if len(parts) > 1:     
          # Extract the first part
          id = '-'.join(parts[:-1])
          variant = parts[-1][-1]
     
     product = Product.objects.get(id=id)
     if variant != 'null':
          product.id = id + "-"+ variant

     cart = Cart(request)
     cart.remove(product)

     total_subtotal = sum(int(item['quantity']) * int(item['price']) for item in cart.cart.values())
     #     return redirect("cart_detail")
     return JsonResponse({
          'success': True,
          'total_subtotal': total_subtotal,  # Include total_subtotal in the response
          })


# @login_required(login_url="/login/")
def item_increment(request, id):
    
     parts = id.split('-')
     variant='null'
     if len(parts) > 1:     
          # Extract the first part
          id = '-'.join(parts[:-1])
          variant = parts[-1][-1]
     
     product = Product.objects.get(id=id)
     if variant != 'null':
          product.id = id + "-"+ variant

     cart = Cart(request)
     
     cart.add(product=product)
     cart_item = cart.cart[str(product.id)]  # Get updated cart item
     total_quantity = len(cart.cart)
     # Calculate sub_total for the current item
     sub_total = int(cart_item['quantity']) * int(product.price)
     total_subtotal = sum(int(item['quantity']) * int(item['price']) for item in cart.cart.values())
     return JsonResponse({
          'success': True,
          'new_quantity': cart_item['quantity'],
          'total_quantity': total_quantity,
          'sub_total': sub_total,
          'total_subtotal': total_subtotal  # Include total_subtotal in the response
     })


# @login_required(login_url="/login/")
def item_decrement(request, id):
     parts = id.split('-')
     variant='null'
     if len(parts) > 1:     
          # Extract the first part
          id = '-'.join(parts[:-1])
          variant = parts[-1][-1]
     
     product = Product.objects.get(id=id)
     if variant != 'null':
          product.id = id + "-"+ variant

     cart = Cart(request)
     cart.decrement(product=product)
     cart_item = cart.cart[str(product.id)]  # Get updated cart item
     total_quantity = len(cart.cart)
     sub_total = int(cart_item['quantity']) * int(product.price)
     total_subtotal = sum(int(item['quantity']) * int(item['price']) for item in cart.cart.values())
     return JsonResponse({
          'success': True,
          'new_quantity': cart_item['quantity'],
          'total_quantity': total_quantity,
          'sub_total': sub_total,
          'total_subtotal': total_subtotal  # Include total_subtotal in the response
     })


# @login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'success': True,'total_subtotal': 0 })


# @login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def place_order(request):
     # Get the current date and time with microsecond precision
     current_time = datetime.now()

     url = reverse('check_order_status')
     
     # Get the protocol (http or https) from the request
     protocol = request.scheme  # This returns 'http' or 'https'

     # Get the domain (including port number if applicable) from the request
     domain = request.get_host()

     # Get the full path of the current URL (excluding domain) from the request
     path = request.get_full_path()

     # Construct the complete URL
     redirect_url = f"{protocol}://{domain}{url}"
     
     # Generate a unique ID using the current date and time
     unique_id = current_time.strftime("%Y%m%d%H%M%S%f")  # YearMonthDayHourMinuteSecondMicrosecond
     cart = request.session.get('cart')
     total =0
     productinfo =""
     for i in cart:
          a = cart[i]['price']
          b = cart[i]['quantity']      
          n = cart[i]['name']      
          total = total + int(a)*b
          productinfo += f"{n},"
          
     print(productinfo)
     if request.method == 'POST':
          
          uid = request.session.get('_auth_user_id')
          user = User.objects.get(id =uid)
          fullname = request.POST.get('fullname')
          email = request.POST.get('email')
          phone = request.POST.get('phone')
          remark = request.POST.get('remark')
          product_info = productinfo
          amount = total
          payment_id = unique_id
         
          order = Order(
               user = user,
               fullname = fullname,
               email = email,
               phone = phone,
               additional_info = remark,
               product_info = product_info,
               amount = amount,
               payment_id = payment_id
          )
          order.save()
          for i in cart:
               a =  (int(cart[i]['price']))
               b = cart[i]['quantity']
              

               total = a*b

               item = OrderItem (
                    Order= order,
                    product = cart[i]['name'],
                    image = cart[i]['image'],
                    quantity = cart[i]['quantity'],
                    price = cart[i]['price'],
                    total = total
               )
               item.save()
          api_url = "https://api.ekqr.in/api/create_order"
          post_data = {
               "key": "6fffda11-f596-4856-8a3c-69e5bb6641ea",
               "client_txn_id": str(payment_id),
               "amount": "1",
               "p_info": product_info,
               "customer_name": fullname,
               "customer_email": email,
               "customer_mobile": phone,
               "redirect_url": redirect_url

          }

          try:
               response = requests.post(api_url, json=post_data)

               if response.status_code == 200:
                    api_response = response.json()
                    if 'payment_url' in api_response['data']:
                         payment_url = api_response['data']['payment_url']
                         return redirect(payment_url)
                    else:
                         return JsonResponse({"error": "Payment URL not found in API response"}, status=500)
          except Exception as e:
               return JsonResponse({"error": str(e)}, status=500)
         
     return render(request, 'checkout.html')


def create_order(request,payment_id="343534433532443", amount="1", product_info="2342sffd", fullname="ssf sdfsd", email="Sfd@sdf.com", phone="8743022455"):
    api_url = "https://api.ekqr.in/api/create_order"
    post_data = {
        "key": "6fffda11-f596-4856-8a3c-69e5bb6641ea",
        "client_txn_id": payment_id,
        "amount": amount,
        "p_info": product_info,
        "customer_name": fullname,
        "customer_email": email,
        "customer_mobile": phone,
        "redirect_url": "check-order-status/"
    }

    try:
        response = requests.post(api_url, json=post_data)

        if response.status_code == 200:
            api_response = response.json()
            if 'payment_url' in api_response['data']:
                payment_url = api_response['data']['payment_url']
                return redirect(payment_url)
            else:
                return JsonResponse({"error": "Payment URL not found in API response"}, status=500)
        else:
            return JsonResponse({"error": "Failed to create order"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def check_order(request):
    # Retrieve client_txn_id and txn_id from GET parameters
    client_txn_id = request.GET.get('client_txn_id')
    txn_id = request.GET.get('txn_id')

    # Ensure both client_txn_id and txn_id are provided
    if client_txn_id is None or txn_id is None:
        return JsonResponse({"error": "client_txn_id and txn_id are required parameters"}, status=400)

    # Define the API endpoint for checking order status
    api_url = "https://api.ekqr.in/api/check_order_status"

    # Prepare the data for the API request
    post_data = {
        "key": "6fffda11-f596-4856-8a3c-69e5bb6641ea",
        "client_txn_id": client_txn_id,
        "txn_date": "15-10-2023"  # You might want to change this to the appropriate date format
    }

    
    try:
        # Make a POST request to the API endpoint
        response = requests.post(api_url, json=post_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the API
            api_response = response.json()

            # Check if the status is "success"
            if api_response.get("data") and api_response.get("data").get("status") == "success":
               orders_to_update = Order.objects.filter(payment_id=client_txn_id)
               orders_to_update.update(paid=True)
            # Return the API response as JSON
          #   return JsonResponse(api_response)
        else:
            # If the request was not successful, return an error response
            return JsonResponse({"error": "Failed to check order status"}, status=500)
    except Exception as e:
        # Handle exceptions, such as network errors or timeouts
        return JsonResponse({"error": str(e)}, status=500)