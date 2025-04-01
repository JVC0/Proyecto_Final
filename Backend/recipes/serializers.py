from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


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
            # "product_group": (
            #     CategorySerializer(instance.category).serialize()
            #     if instance.category
            #     else None
            # ),
        }
