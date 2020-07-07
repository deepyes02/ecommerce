from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here
#store.html view
def store(request):
  data = cartData(request)

  cartItems = data['cartItems']
  products = Product.objects.all()
  context = {'products':products, 'cartItems': cartItems}
  return render(request, 'store/store.html', context)

#cart.html view
def cart(request):
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  context = {'items':items, 'order':order, 'cartItems': cartItems}
  return render(request, 'store/cart.html', context)

#checkout.html view
def checkout(request):
  data = cartData(request)

  cartItems = data['cartItems']
  order = data['order']
  items = data['items']
  context = {'items':items, 'order':order, 'cartItems': cartItems}
  return render(request, 'store/checkout.html', context)

def updateItem(request):
  data = json.loads(request.body)

  productId = data['productId']
  action = data['action']
  print('Action:', action)
  print('productId', productId)
  customer = request.user.customer
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action =='remove':
    orderItem.quantity = (orderItem.quantity - 1)
  orderItem.save()
  if orderItem.quantity <= 0:
    orderItem.delete()

  return JsonResponse("Item was added", safe=False)

def processOrder(request):
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)
  #adding info to the database for logged user
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

  #adding info to the database for unlogged user
  else:
    print("User is not logged in")
    print("cookies: ", request.COOKIES)
    #get the name and email
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
      product = Product.objects.get(id=item['product']['id'])
      orderItem = OrderItem.objects.create(
        product=product,
        order=order,
        quantity=item['quantity']
      )
  ##position of this block has changed from before.
  #logic: regardless of logged in or not logged in,
  #we use the confirm total and make sure everything
  #is correct
  total = float(data['form']['total'])
  order.transaction_id = transaction_id

  if total == float(order.get_cart_total):
    order.complete = True
  order.save()

  if order.shipping == True:
      ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode']
      )

  return JsonResponse("Payment Complete!", safe=False)