from django.contrib.admin import AdminSite
from django.test import TestCase
from django.urls import reverse
from ninja.testing import TestClient
from httpx import AsyncClient

from matrix_api.admin import MatrixAdmin
from matrix_api.forms import MatrixForm
from matrix_api.models import Matrix
from matrix_api.views import api, router


class MatrixFormTestCase(TestCase):
    def test_valid_matrix_text(self):
        form_data = {
            "matrix_text":
                "+-----+-----+-----+-----+\n"
                "|  10 |  20 |  30 |  40 |\n"
                "+-----+-----+-----+-----+\n"
                "|  50 |  60 |  70 |  80 |\n"
                "+-----+-----+-----+-----+\n"
                "|  90 | 100 | 110 | 120 |\n"
                "+-----+-----+-----+-----+\n"
                "| 130 | 140 | 150 | 160 |\n"
                "+-----+-----+-----+-----+"
        }
        form = MatrixForm(data=form_data)
        self.assertEqual(form.data, form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_empty_matrix_text(self):
        form_data = {
            "matrix_text": ""
        }
        form = MatrixForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required", form.errors['matrix_text'][0])

    def test_invalid_number_of_columns(self):
        form_data = {
            'matrix_text': '1 2 \n 3 4 5 \n 6 7 8'
        }
        form = MatrixForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("matrix_text", form.errors)
        self.assertIn("Matrix rows must have the same number of columns", form.errors["matrix_text"])

    def test_invalid_matrix_data(self):
        form_data = {
            'matrix_text': '1 2 3\na b c\n4 5 6'
        }
        form = MatrixForm(data=form_data)
        self.assertTrue(form.errors)
        self.assertIn("Matrix must be square (N*N)", form.errors["matrix_text"])


class MatrixAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.matrix_admin = MatrixAdmin(Matrix, self.site)

    def test_matrix_admin_form(self):
        self.assertEqual(self.matrix_admin.form, MatrixForm)

    def test_save_matrix(self):
        matrix = {
            "matrix_text": "1 2 4 \n 3 4 5 \n 6 7 8"
        }
        form = MatrixForm(data=matrix)
        self.assertTrue(form.is_valid())
        form.save()
        saved_matrix = Matrix.objects.first()
        self.assertEqual(saved_matrix.matrix_text, matrix["matrix_text"])


class TraverseMatrixDb(TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_matrix_save_db(self):
        form_data = {
            "matrix_text":
                "+-----+-----+-----+-----+\n"
                "|  10 |  20 |  30 |  40 |\n"
                "+-----+-----+-----+-----+\n"
                "|  50 |  60 |  70 |  80 |\n"
                "+-----+-----+-----+-----+\n"
                "|  90 | 100 | 110 | 120 |\n"
                "+-----+-----+-----+-----+\n"
                "| 130 | 140 | 150 | 160 |\n"
                "+-----+-----+-----+-----+"
        }
        Matrix.objects.create(**form_data)
        response = self.client.get("/matrix-traversal-db/")
        traversal = [
            10, 50, 90, 130,
            140, 150, 160, 120,
            80, 40, 30, 20,
            60, 100, 110, 70,
        ]
        self.assertEqual(response.status_code, 200)
        self.assertIn(traversal, response.json())

    def test_matrix_db(self):
        matrix1 = {
            "matrix_text": "1 2 \n 2 3"
        }
        matrix2 = {
            "matrix_text": "1 2 3 4\n 5 6 7 8\n 9 10 11 12\n 13 14 15 16"
        }
        Matrix.objects.create(**matrix1)
        Matrix.objects.create(**matrix2)
        response = self.client.get("/matrix-traversal-db/")
        result = [
            [1, 2, 3, 2],
            [1, 5, 9, 13, 14, 15, 16, 12, 8, 4, 3, 2, 6, 10, 11, 7]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, response.json())
