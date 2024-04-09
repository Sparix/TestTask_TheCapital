from django.urls import path
from matrix_api.views import api

urlpatterns = [
    path("matrix/", api.urls),
]
