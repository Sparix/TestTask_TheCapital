from django import forms

from matrix_api.models import Matrix, validations_matrix


class MatrixForm(forms.ModelForm):
    class Meta:
        model = Matrix
        fields = ["matrix_text"]

    def clean_matrix_text(self):
        matrix = self.cleaned_data["matrix_text"]
        return validations_matrix(matrix)
