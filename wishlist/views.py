from django.shortcuts import render, redirect, get_object_or_404
from store.models import Category, SubCategory, Product
from . models import Wishlist
from cart.cart import Cart
from .wishlist import Wishlistitem

cats = Category.objects.all()
subs = SubCategory.objects.all()

def wishlist(request):
    wishlist = Wishlistitem(request)
    if not request.user.username:
        return redirect('users:login')
    cart = Cart(request)
    wishlist_items = Wishlist.objects.filter(user_id=request.user.id)
    # product_ids = wishlist_items.values_list('product_id', flat=True)
    # product_inlist = Product.objects.filter(id__in=product_ids)
    # wishlist_len = len(wishlist_items)

    return render(request, 'wishlist/wishlist.html',{
        'wishlist_items': wishlist_items,
        'cats': cats,
        'subs': subs,
        'cart': cart,
        'wishlist': wishlist,
    })


def add(request):
    if not request.user.username:
        return redirect('users:login')

    if request.POST.get('product_id'):
        wishlist = Wishlist()
        wishlist.quantity = 1
        wishlist.product_id = request.POST.get('product_id')
        id = Product.objects.get(id=wishlist.product_id)
        wishlist.name = id.name
        wishlist.price = id.price
        wishlist.image_product = id.image_product
        wishlist.user_id = request.user.id
        wishlist.save()

    return redirect('wishlist:wishlist')

def remove(request):
    if request.POST.get('wishlist_id'):
        print('test')
        wishlist_new = Wishlist.objects.get(id=request.POST.get('wishlist_id'))
        wishlist_new.delete()
        
    
    return redirect('wishlist:wishlist')