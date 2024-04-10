from django.core.exceptions import ValidationError
from django.db import models


def validations_matrix(matrix):
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

    num_rows = len(rows)
    num_cols = len(rows[0]) if rows else 0
    if num_rows != num_cols:
        raise ValidationError("Matrix must be square (N*N)")

    return matrix


class Matrix(models.Model):
    matrix_text = models.TextField(verbose_name="Text Representation of Matrix")

    def __str__(self):
        return self.matrix_text

    def clean(self):
        super().clean()
        return validations_matrix(self.matrix_text)
