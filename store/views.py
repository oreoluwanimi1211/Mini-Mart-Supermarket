from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, WishList, WishListItem
from category.models import Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug !=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('created_date')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('created_date')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    context = {
    'products': paged_products,
    'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
    'single_product':single_product,
    'in_cart': in_cart,
    
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = Product.objects.none()
    product_count = 0
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count = products.count()
        
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

# @login_required(login_url='login')
# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if product.user_wishlist.filter(id=request.user.id).exists():
#         product.user_wishlist.remove(request.user)
#     else:
#         product.user_wishlist.add(request.user)
#     return HttpResponseRedirect(request.META["HTTP_REFERER"])

# def wishlist(request):
#         return render(request, 'store/wishlists.html')

@login_required(login_url='login')
def add_to_wishlist(request, product_id ):
    
    product = get_object_or_404( Product,id=product_id)
    wishlist, create = WishList.objects.get_or_create(user=request.user)
    wishlistitem = WishListItem.objects.get_or_create(
        wishlist=wishlist,
        product = product,
    )
    return redirect('wishlist')

@login_required
def remove_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(WishList, user=request.user)
    wishlist_item = WishListItem.objects.filter(
        product=product,
        wishlist=wishlist,
    )
    wishlist_item.delete()
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist, create = WishList.objects.get_or_create(user=request.user)
    item = wishlist.items.select_related('product')
   
    context = {
        'item':item,
        'wishlist':wishlist,
    }
    return render(request, 'store/wishlists.html', context)