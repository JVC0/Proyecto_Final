from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class CommentSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "description": instance.description,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "user": (UserSerializer(instance.user).serialize()),
        }
