
from shared.serializers import BaseSerializer

class ProductSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        serialized_data = {
            'id': instance.pk,
            'category': instance.get_category_display(),
            'name': instance.name,   
            'stock': instance.stock,
            'description': instance.description,
            'price': float(instance.price),
            
        }

        if instance.image:
            serialized_data['image'] = self.build_url(instance.image.url)
        else:
            serialized_data['image'] = None  

        return serialized_data

