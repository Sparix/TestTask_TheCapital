from django import forms
from django.core.exceptions import ValidationError

from .models import Matrix


class MatrixForm(forms.ModelForm):
    class Meta:
        model = Matrix
        fields = ["matrix_text"]

    def clean_matrix_text(self):
        matrix = self.cleaned_data["matrix_text"]

        lines = matrix.split("\n")
        if not lines:
            raise ValidationError("Matrix data cannot be empty")

        rows = []
        for line in lines:
            numbers = [int(num) for num in line.split() if num.isdigit()]
            if numbers:
                rows.append(numbers)

        row_lengths = set(len(row) for row in rows)
        if len(row_lengths) != 1:
            raise ValidationError("Matrix rows must have the same number of columns")

        for row in rows:
            for cell in row:
                if not isinstance(cell, int):
                    raise ValidationError("Matrix data must contain only integers")

        return matrix
