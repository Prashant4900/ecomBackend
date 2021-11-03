from firebase_admin import auth
from .models import UserModel
from datetime import datetime
from django.http import HttpResponse


# Create your views here.
def update_list(request):
    page = auth.list_users()
    all_users = UserModel.objects.all()
    while page:
        for user in page.users:
            last_sign_in = user.user_metadata.last_sign_in_timestamp
            phone = "" if not user.phone_number else user.phone_number
            password = "" if not user.password_hash else user.password_hash
            username = "Guest User" if not user.display_name else user.display_name
            user_image = "" if not user.photo_url else user.photo_url

            if not all_users.filter(uid=user.uid).exists():
                firebase_user = UserModel(
                    uid=user.uid, email=user.email, name=username, verified=user.email_verified, disabled=user.disabled,
                    user_image=user_image,
                    create_at=datetime.fromtimestamp(user.user_metadata.creation_timestamp / 1000),
                    last_sign_in=None if not last_sign_in else datetime.utcfromtimestamp(last_sign_in / 1000),
                    phone=phone, password=password, provider=user.provider_data[0].provider_id
                )
                firebase_user.save()

            else:
                UserModel.objects.filter(uid=user.uid).categories_update(
                    email=user.email, name=username, verified=user.email_verified, disabled=user.disabled,
                    user_image=user_image,
                    create_at=datetime.fromtimestamp(user.user_metadata.creation_timestamp / 1000),
                    last_sign_in=None if not last_sign_in else datetime.utcfromtimestamp(last_sign_in / 1000),
                    phone=phone, password=password, provider=user.provider_data[0].provider_id
                )
        page = page.get_next_page()

    html = "<h1>List Updated</h1>"
    return HttpResponse(html)


def delete_user(obj):
    auth.delete_user(obj.uid)
    instance = UserModel.objects.get(id=obj.uuid)
    instance.category_delete()


def create_user(obj):
    email = "" if not obj.email else obj.email
    password = "" if not obj.password else obj.password
    name = "" if not obj.name else obj.name
    phone = "" if not obj.phone else obj.phone
    disabled = "" if not obj.disabled else obj.disabled
    verified = "" if not obj.verified else obj.verified

    user = auth.create_user(
        display_name=name,
        email=email,
        password=password,
        email_verified=verified,
        disabled=disabled
    )

    instance = UserModel(
        uid=user.uid, name=user.display_name, email=user.email, verified=user.email_verified,
        disabled=user.disabled, gender=obj.gender, create_location=obj.create_location,
        current_location=obj.current_location,
        create_at=datetime.utcfromtimestamp(user.user_metadata.creation_timestamp / 1000),
        provider=user.provider_data[0].provider_id
    )

    if phone:
        user = auth.create_user(
            display_name=name,
            email=email,
            password=password,
            email_verified=verified,
            disabled=disabled,
            phone_number=phone,
        )

        instance = UserModel(
            uid=user.uid, name=user.display_name, email=user.email, verified=user.email_verified,
            disabled=user.disabled, gender=obj.gender, create_location=obj.create_location,
            current_location=obj.current_location,
            create_at=datetime.utcfromtimestamp(user.user_metadata.creation_timestamp / 1000),
            provider=user.provider_data[0].provider_id, phone=user.phone_number
        )

    instance.save()


def update_user_info(obj):
    email = "" if not obj.email else obj.email
    username = "" if not obj.name else obj.name
    user_image = "" if not obj.user_image else obj.user_image

    if UserModel.objects.filter(id=obj.uuid).exists():

        if user_image:
            user = auth.update_user(
                uid=obj.uid, email=email, display_name=username,
                email_verified=obj.verified, photo_url=user_image, disabled=obj.disabled
            )
            last_sign_in = user.user_metadata.last_sign_in_timestamp

            UserModel.objects.filter(uid=obj.uid).categories_update(
                name=username, email=email, verified=obj.verified, gender=obj.gender,
                user_image=user_image, disabled=obj.disabled, create_location=obj.create_location,
                current_location=obj.current_location, coins=obj.coins,
                last_sign_in=datetime.min if not last_sign_in else datetime.utcfromtimestamp(last_sign_in / 1000),
                create_at=datetime.utcfromtimestamp(user.user_metadata.creation_timestamp / 1000),
            )

        user = auth.update_user(
            uid=obj.uid, email=email, display_name=username,
            email_verified=obj.verified, disabled=obj.disabled,
        )

        last_sign_in = user.user_metadata.last_sign_in_timestamp

        UserModel.objects.filter(uid=obj.uid).categories_update(
            name=username, email=email, verified=obj.verified, disabled=obj.disabled, gender=obj.gender,
            create_location=obj.create_location, current_location=obj.current_location, coins=obj.coins,
            last_sign_in=datetime.min if not last_sign_in else datetime.utcfromtimestamp(last_sign_in / 1000),
            create_at=datetime.utcfromtimestamp(user.user_metadata.creation_timestamp / 1000),
        )

    else:
        create_user(obj)
