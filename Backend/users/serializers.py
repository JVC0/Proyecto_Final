from shared.serializers import BaseSerializer


class TokenSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "user": UserSerializer(instance.user).serialize(),
            "key": str(instance.key),
            "created_at": instance.created_at.isoformat(),
        }


class UserSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "username": instance.username,
        }


class ProfileSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            "id": instance.pk,
            "avatar": self.build_url(instance.avatar.url),
            "bio": instance.bio,
            "user": UserSerializer(instance.user, request=self.request).serialize(),
        }
