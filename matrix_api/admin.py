from django.contrib import admin
from .models import Matrix
from matrix_api.forms import MatrixForm


@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    form = MatrixForm
