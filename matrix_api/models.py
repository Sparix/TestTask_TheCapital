from django.db import models


class Matrix(models.Model):
    matrix_text = models.TextField(verbose_name="Text Representation of Matrix")

    def __str__(self):
        return self.matrix_text
