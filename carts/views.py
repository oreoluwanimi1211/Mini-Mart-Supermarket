from django.shortcuts import get_object_or_404,render, redirect
from store.models import Product, Variation
from django.http import HttpResponse
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def _cart_id(request): # create this step one 
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                # print(variation)
            except:
                pass
        
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        # get the cart by using the session ID
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

# combine both product and cart to get cart item
    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        
        ''' grouping of cart items '''
        # exiting variation --> database
        
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        
        
        if product_variation in existing_variation_list:
            # increase cart quantity
            index = existing_variation_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # create new cart item
            # current variation --> product_variation
            # item_id --> database
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            
            item.save()
    else:
        cart_item = CartItem.objects.create(
        product=product, 
        quantity=1, 
        cart=cart
        )
        ''' adding variation to a cart item '''
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for  items in cart_items:
            total += (items.product.price * items.quantity)
            quantity += items.quantity
    except ObjectDoesNotExist:
        pass # Dont do anything
    
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request, 'store/cart.html', context)

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        # if request.user.is_authenticated:
        #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        # else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item .quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def delete_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')