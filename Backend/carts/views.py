import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product
from shared.decorators import check_method

from .decorators import card_checker, validate_quantity
from .models import Cart, CartItem
from .serializers import CartSerializer


@check_method("POST")
@ensure_csrf_cookie
@validate_quantity
def add_to_cart(request, product_id):
    data = json.loads(request.body)
    quantity = data.get("quantity")
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(profile=request.user.profile)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )

    if not item_created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            return JsonResponse(
                {"message": "The total quantity would exceed available stock"},
                status=400,
            )
        cart_item.quantity = new_quantity
        cart_item.save()

    return JsonResponse({"message": "Item added to cart successfully"})


@check_method("DELETE")
@ensure_csrf_cookie
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, profile=request.user.profile)
    cart_item = get_object_or_404(CartItem, cart=cart, id=product_id)
    cart_item.delete()
    return JsonResponse({"message": "item has been deleted"})


@check_method("GET")
def cart_detail(request):
    cart = get_object_or_404(Cart, profile=request.user.profile)
    serializer = CartSerializer(cart, request=request)
    return serializer.json_response()


@check_method("POST")
@card_checker
def payment(request):
    cart = Cart.objects.get(profile=request.user.profile)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return JsonResponse({"message": "No items in the cart"}, status=400)
    for cart_item in cart_items:
        product = Product.objects.get(name=cart_item.product)
        product.stock -= cart_item.quantity
        product.save()
        cart_item.delete()
    return JsonResponse({"message": "Payment successful"})
