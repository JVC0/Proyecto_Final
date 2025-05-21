from products.serializers import ProductSerializer
from shared.serializers import BaseSerializer
from users.serializers import ProfileSerializer


class CartItemSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "quantity": instance.quantity,
            "product": ProductSerializer(
                instance.product, request=self.request
            ).serialize(),
        }


class CartSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "profile": ProfileSerializer(
                instance.profile, request=self.request
            ).serialize(),
            "total_price": float(instance.total_price),
            "items": CartItemSerializer(
                instance.cartitems.all(), request=self.request
            ).serialize(),
        }
