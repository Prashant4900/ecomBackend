from .json import category_to_json, product_to_json
from products.models import CategoryModel, ProductsModel
from .constant import products_ref, category_ref


def categories_update(obj):
    if not obj.uuid:
        data = category_ref.push()
        json1 = category_to_json(data.key, obj)
        data.update(json1)
    else:
        data = category_ref.child(obj.uuid)
        json1 = category_to_json(data.key, obj)
        data.update(json1)
    if not CategoryModel.objects.filter(uuid=data.key).exists():
        instance = CategoryModel(
            uuid=data.key, name=obj.name,
            created_at=obj.created_at, updated_at=obj.updated_at
        )
        instance.save()
    else:
        CategoryModel.objects.filter(uuid=data.key).update(name=obj.name, updated_at=obj.updated_at)


def products_update(obj):
    if not obj.uuid:
        data = products_ref.push()
        json1 = product_to_json(data.key, obj)
        data.update(json1)
    else:
        data = products_ref.child(obj.uuid)
        json1 = product_to_json(data.key, obj)
        data.update(json1)
    if not ProductsModel.objects.filter(uuid=data.key).exists():
        instance = ProductsModel(
            uuid=data.key, name=obj.name, image=obj.image,
            description=obj.description, category=obj.category,
            price=obj.price, discount=obj.discount, offer=obj.offer,
            created_at=obj.created_at, updated_at=obj.updated_at
        )
        instance.save()
    else:
        ProductsModel.objects.filter(uuid=data.key).update(
            name=obj.name, image=obj.image,
            description=obj.description, category=obj.category,
            price=obj.price, discount=obj.discount, offer=obj.offer,
            updated_at=obj.updated_at
        )
