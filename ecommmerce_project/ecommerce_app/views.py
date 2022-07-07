
from unicodedata import category
from urllib import response
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
import requests as HTTP_Client
from django.contrib import messages
from django.utils import timezone
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import pprint
import os
from .models import *
from .utils import *

# default page when loading
def index(request):
    response = render(request, 'ecommerce_app/home.html')
    return response

# to get the inventory list from the html page
def product(request):
    items = Product.objects.all()
    data = {'items': items}
    response = render(request, 'ecommerce_app/product-page.html', data)
    return response

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    response = render(request, 'ecommerce_app/store.html', context)
    return response

# get the cart html page
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    response = render(request, 'ecommerce_app/checkout.html', context)
    return response

# get the cart html page
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}

    response = render(request, 'ecommerce_app/cart.html', context)
    return response

def item(request, pk):
	product = Product.objects.get(id=pk)

	if request.method == 'POST':
		product = Product.objects.get(id=pk)
		#Get user account information
		try:
			customer = request.user.customer	
		except:
			device = request.COOKIES['device']


		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		orderItem.quantity=request.POST['quantity']
		orderItem.save()

		return redirect('cart')

	context = {'product':product}
	return render(request, 'ecommerce/product.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})

# get the icon when item is out of stock
def get_icon(request, name):
    auth = OAuth1(os.environ["apikey"], os.environ["privatekey"])
    endpoint = f"http://api.thenounproject.com/icon/{name}"

    API_response = HTTP_Client.get(endpoint, auth=auth)
    responseJSON = API_response.json()
    # print(API_response.content)
    # print(responseJSON)
    # pp.pprint(responseJSON)
    icon = (responseJSON['icon']['preview_url'])
    if os.environ['env'] == 'prod':
        # send emails, only ibn prod
        pass
    # response = render(request, 'wishes_app/wishes.html', {"icon": icon})
    # return response


