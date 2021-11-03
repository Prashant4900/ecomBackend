from products.models import CategoryModel, ProductsModel
from .constant import products_ref, category_ref


def category_delete(obj):
    category_ref.child(obj.uuid).delete()
    instance = CategoryModel.objects.get(uuid=obj.uuid)
    instance.delete()


def products_delete(obj):
    products_ref.child(obj.uuid).delete()
    instance = ProductsModel.objects.get(uuid=obj.uuid)
    instance.delete()
