from firebase_admin import db

ref = db.reference()
category_ref = ref.child("categories")
products_ref = ref.child("products")