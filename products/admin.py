from django.contrib import admin
from .models import CategoryModel, ProductsModel
from .operations.update import categories_update, products_update
from .operations.delete import category_delete, products_delete


# Register your models here.
@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'created_at', 'updated_at')
    list_display_links = ('uuid', 'name')
    readonly_fields = ('uuid',)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    list_per_page = 10
    save_on_top = True

    def get_actions(self, request):
        pass

    def save_model(self, request, obj, form, change):
        categories_update(obj)

    def delete_model(self, request, obj):
        category_delete(obj)


@admin.register(ProductsModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description', 'category', 'price', 'offer')
    list_display_links = ('uuid', 'name', 'description')
    readonly_fields = ('image_preview', 'uuid',)
    search_fields = ('name', 'category', 'price', 'offer', 'discount')
    list_filter = ('offer', 'category', 'created_at', 'updated_at')
    list_per_page = 10
    save_on_top = True

    def get_actions(self, request):
        pass

    def save_model(self, request, obj, form, change):
        products_update(obj)

    def delete_model(self, request, obj):
        products_delete(obj)
