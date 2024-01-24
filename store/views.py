from django.shortcuts import render
from .models import Product,Customer,Order,OrderItem, ShippingAddress
from django.http import JsonResponse
import json
import datetime

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created  = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()
        cartitem = order.total_cart_item

    else:
        item=[]
        order = {"total_cart_item":0,"total_cart_price":0, "shipping":False}
        cartitem = order['total_cart_item']




    products = Product.objects.all()

    context ={"products":products, "cartitem":cartitem}
    return render(request, 'store/store.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created  = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart', cart)
        item=[]
        order = {"total_cart_price":0, "total_cart_item":0, "shipping":False}
        cartitem = order['total_cart_item']

        for i in cart:
            cartitem += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['total_cart_price'] += total
            order['total_cart_item'] += cart[i]['quantity']

            it = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image_url
                },
                'quantity': cart[i]['quantity'],
                'cart_total':total
            }

            item.append(it)



    context ={"items":item, "order":order, "cartitem":cartitem}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created  = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()

    else:
        item=[]
        order = {"total_cart_item":0,"total_cart_price":0, "shipping":False}
        cartitem = order['total_cart_item']


    context ={"items":item, "order":order, "cartitem":cartitem}
    

    
    return render(request, 'store/checkout.html', context)


def updateCart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    

    customer = request.user.customer
    products_id = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)


    orderitem , created = OrderItem.objects.get_or_create(order=order, product=products_id)
    print(orderitem)

    if action =="add":
        orderitem.quantity = (orderitem.quantity + 1)
    
    elif action == "remove":
        orderitem.quantity = (orderitem.quantity -1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
  


    return JsonResponse( "item added to cart", safe=False)





def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['userFormData']['total'])
        order.transaction_id = transaction_id


        if total == order.total_cart_price:
            order.complete = True
        
        order.save()


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shippingInfo']['address'],
                city = data['shippingInfo']['city'],
                state = data['shippingInfo']['state'],
                zipcode = data['shippingInfo']['zipcode'],

            )


 

    return JsonResponse("payment complete", safe=False)





def cartsView(request):

    if request.user.is_authenticated:

        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()

    else:
        item = []



    context = {'items':item, 'order':order}
    return render(request, 'store/carts.html', context)


def checkoutsView(request):

    if request.user.is_authenticated:

        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.all()

    else:
        item=[]
        order = {'total_cart_price':0, 'total_cart_price':0}


    context = {'items':item, 'order':order}
    return render(request, 'store/checkouts.html', context)



def UpdateItem(request):

    data = json.loads(request.body)
    print(data)
    product_id = data['product_id']
    action = data['action']
    

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem , created = OrderItem.objects.get_or_create(order=order, product=product)

 

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == "remove":
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()






    return JsonResponse("item added success", safe=False)



def processDataView(request):
    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)
    customer = request.user.customer
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['data']['total'])
        order.transaction_id = transaction_id

        if total == order.total_cart_price:
            order.save()

        if order.shipping != "False":
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address = data['shipping']['address'],
                state = data['shipping']['state'],
                city= data['shipping']['city'],
                zipcode = data['shipping']['zipcode']

            )




    return JsonResponse("process view ", safe=False)