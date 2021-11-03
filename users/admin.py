from django.contrib import admin
from .models import UserModel
from .views import delete_user, update_user_info


# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'email', 'gender', 'coins',
                    'provider', 'verified', 'last_sign_in',)
    list_display_links = ('uid', 'name', 'email')
    search_fields = ('uid', 'name', 'email',
                     'provider', 'verified', 'disabled')
    list_per_page = 50
    readonly_fields = (
        'provider', 'uid', 'phone', 'image_preview', 'last_sign_in', 'create_at', 'create_location', 'current_location',
        'coins'
    )
    fieldsets = (
        (
            None, {
                'fields': ['uid', 'email', 'password']
            }
        ),
        (
            "Personal Information", {
                'fields': ['name', 'phone', 'gender', 'user_image', 'image_preview', 'provider', 'create_location',
                           'current_location']
            }
        ),
        (
            "Rewards", {
                'fields': ['coins']
            }
        ),
        (
            "Permissions", {
                'fields': ['verified', 'disabled']
            }
        ),
        (
            "Important dates", {
                'fields': ['last_sign_in', 'create_at']
            }
        ),
    )
    save_on_top = True

    list_filter = (
        ('provider', admin.AllValuesFieldListFilter),
        ('gender', admin.AllValuesFieldListFilter),
        ('create_location', admin.AllValuesFieldListFilter),
        ('current_location', admin.AllValuesFieldListFilter),
        'verified',
        'disabled',
        ("phone", admin.EmptyFieldListFilter),
        ("user_image", admin.EmptyFieldListFilter),
        'create_at',
        'last_sign_in',
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields + ('user_image', 'phone')
        return self.readonly_fields + ('password',)

    def delete_model(self, request, obj):
        delete_user(obj)

    def save_model(self, request, obj, form, change):
        update_user_info(obj=obj)

    def get_actions(self, request):
        pass
