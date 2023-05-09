from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from cart.cart import Cart
from cart.vnpay import vnpay, get_client_ip
from store.models import Product
from store.views import cats, subs
from users.models import Customer
from . models import Order, OrderItem
from datetime import datetime
from wishlist.wishlist import Wishlistitem


def cart_detail(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)

    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for c in cart:
            product = c['product']
            quantity_new = int(request.POST.get('quantity_'+str(product.id)))
            if quantity_new != 0:
                product_cart = {
                    str(product.id): {
                        'quantity': quantity_new,
                        'price': str(product.price),
                    }
                }
                cart_new.update(product_cart)
                c['quantity'] = quantity_new

        request.session['cart'] = cart_new

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'wishlist': wishlist,
        'cats': cats,
        'subs': subs,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')), size=request.POST.get('size'), color=request.POST.get('color'))

    return redirect('cart:cart_detail')


@require_POST
def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')
 

def checkout(request):

    if not request.user.username:
        return redirect('users:login')

    cart = Cart(request)
    wishlist = Wishlistitem(request)
    customer = Customer.objects.get(user__id=request.user.id)
    tel = customer.tel
    address = customer.address

    if request.POST.get('btnOrder'):
        if request.POST.get('orther-address'):
            if request.POST.get('payment_directcheck'):
                order = Order()
                order.username = request.user.username
                order.last_name = request.POST.get('second_last_name')
                order.first_name = request.POST.get('second_first_name')
                order.tel = request.POST.get('second_tel')
                order.address = request.POST.get('second_address')
                order.total = cart.get_final_total_price()
                order.status = True
                order.save()
                for c in cart:
                    OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'], size=c['size'], color=c['color'])
                
                cart.clear()
                
                return redirect('cart:success')

            elif request.POST.get('payment_banktransfer'):
                order = Order()
                order.username = request.user.username
                order.last_name = request.POST.get('second_last_name')
                order.first_name = request.POST.get('second_first_name')
                order.tel = request.POST.get('second_tel')
                order.address = request.POST.get('second_address')
                order.total = cart.get_final_total_price()
                order.save()

                for c in cart:
                    OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'])
                ipaddr = get_client_ip(request)

                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.1.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = int(order.total)*100
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + str(order.id)
                vnp.requestData['vnp_OrderInfo'] = 'Thanh toán đơn hàng ' + str(order.id) + ' vào lúc ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                vnp.requestData['vnp_OrderType'] = 'Thanh toán hóa đơn'
                vnp.requestData['vnp_Locale'] = 'vn'
                vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
                vnp.requestData['vnp_IpAddr'] = ipaddr
                vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
                vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)


                cart.clear()

                return redirect(vnpay_payment_url)
        else:
            if request.POST.get('payment_directcheck'):
                order = Order()
                order.username = request.user.username
                order.last_name = request.user.last_name
                order.first_name = request.user.first_name
                order.tel = tel
                order.address = address
                order.total = cart.get_final_total_price()
                order.status = True
                order.save()
                for c in cart:
                    OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'], size=c['size'], color=c['color'])

                cart.clear()

                return redirect('cart:success')

            elif request.POST.get('payment_banktransfer'):
                order = Order()
                order.username = request.user.username
                order.last_name = request.user.last_name
                order.first_name = request.user.first_name
                order.tel = tel
                order.address = address
                order.total = cart.get_final_total_price()
                order.save()

                for c in cart:
                    OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'])
                ipaddr = get_client_ip(request)

                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.1.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = int(order.total)*100
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S') + str(order.id)
                vnp.requestData['vnp_OrderInfo'] = 'Thanh toán đơn hàng ' + str(order.id) + ' vào lúc ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                vnp.requestData['vnp_OrderType'] = 'Thanh toán hóa đơn'
                vnp.requestData['vnp_Locale'] = 'vn'
                vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
                vnp.requestData['vnp_IpAddr'] = ipaddr
                vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
                vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)


                cart.clear()

                return redirect(vnpay_payment_url)

    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'wishlist': wishlist,
        'address': address,
        'tel': tel,
        'cats': cats,
        'subs': subs,
    })


def success(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount'])/100 
        order_desc = inputData['vnp_OrderInfo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_CardType = inputData['vnp_CardType']
        vnp_BankCode = inputData['vnp_BankCode']

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                order = Order()
                order.status = True
                return render(request, 'cart/result.html', {
                    "result": "Thanh toán thành công",
                    "amount": amount,
                    "order_desc": order_desc,
                    "CardType": vnp_CardType,
                    "BankCode": vnp_BankCode,
                    "cart": cart,
                    "wishlist": wishlist,
                })
            else:
                 return render(request, 'cart/result.html', {
                    "result": "Thanh toán không thành công",
                    "amount": amount,
                    "order_desc": order_desc,
                    "CardType": vnp_CardType,
                    "BankCode": vnp_BankCode,
                    "cart": cart,
                    "wishlist": wishlist,
                })
    else:
        order_desc = 'đặt đơn hàng' + ' vào lúc ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        return render(request, 'cart/result.html', {
                    "result": "Đặt hàng thành công",
                    "order_desc": order_desc,
                    "cart": cart,
                    "wishlist": wishlist,        
                })

    return render(request, 'cart/result.html',{
        'cats': cats,
        'subs': subs,
        'cart': cart,
        'wishlist': wishlist,   
    })
