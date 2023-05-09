from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . models import Category, SubCategory, Product, Image, Contact
from . form import FormContact
from cart.cart import Cart
from wishlist.wishlist import Wishlistitem

cats = Category.objects.all()
subs = SubCategory.objects.all()

    
def index(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)
    new_products = Product.objects.all().order_by('-public_day')[:8]

    return render(request, 'store/index.html',{
        'cats': cats,
        'subs': subs,
        'new_products': new_products,
        'cart': cart,
        'wishlist': wishlist,
    })


def shop(request, slug):
    cart = Cart(request)
    wishlist = Wishlistitem(request)
    cat = cats.values_list('slug')
    sub = subs.values_list('slug')
    category = ''
    subcategory = ''
    if slug == 'all':
        products = Product.objects.all()
        category = 'Cửa hàng'

    elif cat.filter(slug=slug).exists():
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.get(slug=slug)

    elif sub.filter(slug=slug).exists():
        products = Product.objects.filter(subcategory__slug=slug)
        category = Category.objects.get(subcategory__slug=slug)
        subcategory = SubCategory.objects.get(slug=slug)

    from_price = 0
    to_price = 0
    product_name = ''
    if request.GET.get('price200'):
        from_price = int(0)
        to_price = int(200000)
        product_name = request.GET.get('product_name')
        if product_name != None and product_name != '':
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price400'):
        from_price = int(200000)
        to_price = int(400000)
        product_name = request.GET.get('product_name')
        if product_name != None and product_name != '':
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price600'):
        from_price = int(400000)
        to_price = int(600000)
        product_name = request.GET.get('product_name')
        if product_name != None and product_name != '':
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price800'):
        from_price = int(600000)
        to_price = int(800000)
        product_name = request.GET.get('product_name')
        if product_name != None and product_name != '':
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price1000'):
        from_price = int(800000)
        to_price = int(1000000)
        product_name = request.GET.get('product_name')
        if product_name != None and product_name != '':
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]


    page = request.GET.get('page', 1)
    paginator = Paginator(products, 20)
    products_pager = paginator.page(page)


    return render(request, 'store/shop.html',{
        'cats': cats,
        'subs': subs,
        'products': products,
        'category': category,
        'subcategory': subcategory,
        'products': products_pager,
        'from_price': from_price,
        'to_price': to_price,
        'cart': cart,
        'wishlist': wishlist,
    })


def detail(request, id):
    cart = Cart(request)
    wishlist = Wishlistitem(request)

    product = Product.objects.get(id=id)
    sub_category_id = Product.objects.filter(id=id).values_list('subcategory')
    same_products = Product.objects.filter(subcategory__in=sub_category_id).exclude(id=id)
    images = Image.objects.filter(product_id=id)
    sub_category_name = SubCategory.objects.get(pk=sub_category_id[0][0])
    # sub_category_size = sub_category_name.size
    size = []
    if str(sub_category_name) == "Ngắn tay" or str(sub_category_name) == "Dài tay":
        for i in range(37, 43):
            size.append(i)
    elif str(sub_category_name) == "Quần tây" or str(sub_category_name) == "Quần kaki":
        for i in range(28, 36):
            size.append(i)
    elif str(sub_category_name) == "Underwear" or str(sub_category_name) == "Quần đùi":
        size = ["M", "L", "XL"]


    avg_vote = product.vote

    full_stars = int(avg_vote)
    half_star = (avg_vote - full_stars) >= 0.5
    empty_stars = 5 - full_stars - half_star
    full = ''
    half = ''
    empty = ''
    for i in range(full_stars):
        full += '''<small class="fas fa-star"></small>'''
    if half_star:
        half = '''<small class="fas fa-star-half-alt"></small>'''
    for i in range(empty_stars):
        empty += '''<small class="far fa-star"></small>'''


    return render(request, 'store/detail.html',{
        'cats': cats,
        'subs': subs,
        'product': product,
        'images': images,
        'same_products': same_products,
        'size': size,
        'cart': cart,
        'wishlist': wishlist,
        'avg_vote': avg_vote,
        'full': full,
        'empty': empty,
        'half': half,
    })


def search(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)
    product_name = ''
    if request.GET.get('product_name'):
        product_name = request.GET.get('product_name')
        search_products = Product.objects.filter(name__contains=product_name)

    from_price = 0
    to_price = 0
    if request.GET.get('price200'):
        from_price = int(0)
        to_price = int(200000)
        product_name = request.GET.get('product_name')
        search_products = [product for product in search_products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price400'):
        from_price = int(200000)
        to_price = int(400000)
        product_name = request.GET.get('product_name')
        search_products = [product for product in search_products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price600'):
        from_price = int(400000)
        to_price = int(600000)
        product_name = request.GET.get('product_name')
        search_products = [product for product in search_products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price800'):
        from_price = int(600000)
        to_price = int(800000)
        product_name = request.GET.get('product_name')
        search_products = [product for product in search_products if from_price <=
                    product.price <= to_price]
    elif request.GET.get('price1000'):
        from_price = int(800000)
        to_price = int(1000000)
        product_name = request.GET.get('product_name')
        search_products = [product for product in search_products if from_price <=
                    product.price <= to_price]

    page = request.GET.get('page', 1)
    paginator = Paginator(search_products, 20)
    products_pager = paginator.page(page)

    return render(request, 'store/shop.html', {
        'products': products_pager,
        'product_name': product_name,
        'cats': cats,
        'subs': subs,
        'cart': cart,
        'wishlist': wishlist,
    })


def contact(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)
    form = FormContact()
    result = ''
    if request.POST.get('button-submit'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()
            result = '''
                    <div class = "col-md-12">
                        <div class="alert alert-success" role="alert">
                            Đã gửi tin nhắn thành công!
                        </div>
                    </div>
                    '''
        else:
            result = '''
                <div class = "col-md-12">
                    <div class="alert alert-danger" role="alert">
                        Vui lòng kiểm tra lại nội dung!
                    </div>
                </div>
                '''

    return render(request, 'store/contact.html', {
        'cats': cats,
        'subs': subs,
        'form': form,
        'result': result,
        'cart': cart,
        'wishlist': wishlist,
    })

def faqs(request):
    cart = Cart(request)
    wishlist = Wishlistitem(request)

    return render(request, 'store/faqs.html', {
        'cats': cats,
        'subs': subs,
        'cart': cart,
        'wishlist': wishlist,
    })