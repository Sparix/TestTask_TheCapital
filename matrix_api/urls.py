from django.urls import path
from ninja import NinjaAPI
from matrix_api.views import router

api = NinjaAPI()

api.add_router("/matrix/", router)  # You can add a router as an object

urlpatterns = [
    path("", api.urls, name="matrix"),
]