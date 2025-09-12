from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """View to display the details of a single product."""
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

@login_required
def add_to_cart(request, pk):
    """Adds a product to the user's cart."""
    product = get_object_or_404(Product, pk=pk)
    
    # User ke liye cart lein ya ek naya banayein
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check karein ki product pehle se cart mein hai ya nahi
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Agar pehle se hai, to quantity badhayein
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    # User ko wapas product ke page par redirect karein
    return redirect('product_detail', pk=pk)

@login_required
def view_cart(request):
    """View to display the user's cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'products/cart.html', context)

@login_required
def remove_from_cart(request, pk):
    """Removes a product from the user's cart."""
    cart_item = get_object_or_404(CartItem, pk=pk)
    # Ensure the user owns the cart item
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('view_cart')
