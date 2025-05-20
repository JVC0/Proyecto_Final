import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product

from .models import Cart, CartItem
from .serializers import CartSerializer


@ensure_csrf_cookie
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    data = json.loads(request.body)
    quantity = data.get("quantity")
    cart, _ = Cart.objects.get_or_create(profile=request.user.profile)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )
    print(item_created)
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({"message": "item has been created"})


@ensure_csrf_cookie
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, profile=request.user.profile)
    cart_item = get_object_or_404(CartItem, cart=cart, id=product_id)
    cart_item.delete()
    return JsonResponse({"message": "item has been deleted"})


def cart_detail(request):
    cart = get_object_or_404(Cart, profile=request.user.profile)
    serializer = CartSerializer(cart, request=request)
    return serializer.json_response()


def payment(request):
    cart = Cart.objects.get(profile=request.user.profile)
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        product = Product.objects.get(name=cart_item.product)
        product.stock -= cart_item.quantity
        product.save()
        cart_item.delete()
    return JsonResponse({"message": "Payment successful"})
