from django.forms.models import model_to_dict
import json


def category_to_json(uuid, obj):

    data = {
        "uuid": uuid,
        "name": obj.name,
        "createdAt": obj.created_at,
        "updatedAt": obj.updated_at,
    }

    instance = json.dumps(data, default=str)
    return json.loads(instance)


def product_to_json(uuid, obj):

    data = {
        'uuid': uuid,
        "name": obj.name,
        "image": obj.image,
        "description": obj.description,
        "category": model_to_dict(obj.category),
        "price": obj.price,
        "discount": obj.discount,
        "offer": obj.offer,
        "createdAt": obj.created_at,
        "updatedAt": obj.updated_at,
    }

    instance = json.dumps(data, default=str)
    return json.loads(instance)
