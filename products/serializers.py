from shared.serializers import BaseSerializer
from categories.serializers import CategorySerializer


class ProductSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "name": instance.name,
            "stock": instance.stock,
            "description": instance.description,
            "price": float(instance.price),
            "image": self.build_url(instance.image.url),
            "category": CategorySerializer(instance.category).serialize(),
        }


class ProductGroupSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "name": instance.name,
            "products": ProductSerializer(
                instance.products, request=self.request
            ).serialize(),
        }
