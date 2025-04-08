from shared.serializers import BaseSerializer
from users.serializers import UserSerializer
from products.serializers import ProductGroupSerializer
from comments.serializers import CommentSerializer


class RecipeSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "name": instance.name,
            "description": instance.description,
            "created_at": instance.created_at.isoformat(),
            "updated_at": instance.updated_at.isoformat(),
            "user": (UserSerializer(instance.user, request=self.request).serialize()),
            "product_group": (
                ProductGroupSerializer(
                    instance.product_group, request=self.request
                ).serialize()
            ),
            "comments": (
                CommentSerializer(
                    instance.comments.all(), request=self.request
                ).serialize()
                if instance.comments
                else None
            ),
        }
