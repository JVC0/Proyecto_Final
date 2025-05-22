import json
import re
from datetime import datetime

from django.http import JsonResponse

from products.models import Product


def validate_quantity(view_func):
    def wrapped(request, product_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            quantity = data.get("quantity")

            product = Product.objects.get(id=product_id)

            if quantity > product.stock:
                return JsonResponse(
                    {
                        "message": f"Cannot add {quantity} items. Only {product.stock} available.",
                    },
                    status=400,
                )

            return view_func(request, product_id, *args, **kwargs)
        except ValueError:
            return JsonResponse(
                {"message": "Quantity must be a valid number."},
                status=400,
            )
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product not found."}, status=404)

    return wrapped


def card_checker(func):
    def wrapper(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            card_number = data.get("card_number", "")
            exp_date = data.get("exp_date", "")
            cvc = data.get("cvc", "")
            if not re.fullmatch(r"^\d{16}$", card_number):
                return JsonResponse(
                    {"mesage": "Invalid card number - must be 16 digits"}, status=400
                )
            if not re.fullmatch(r"^\d{4}$", exp_date):
                return JsonResponse(
                    {"mesage": "Invalid expiration date - must be MMYY format"},
                    status=400,
                )
            month = int(exp_date[:2])
            year = 2000 + int(exp_date[2:])
            if month < 1 or month > 12:
                return JsonResponse({"mesage": "Invalid month"}, status=400)
            expiry_date = datetime(year, month, 1)
            if expiry_date < datetime.now():
                return JsonResponse({"mesage": "Card expired"}, status=400)
            if not re.fullmatch(r"^\d{3}$", cvc):
                return JsonResponse(
                    {"mesage": "Invalid CVC - must be 3 digits"}, status=400
                )
            return func(request, *args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({"mesage": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"mesage": f"Validation error: {str(e)}"}, status=400)

    return wrapper
