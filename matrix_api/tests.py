from django.contrib.admin import AdminSite
from unittest.mock import patch
from ninja.testing import TestClient
from matrix_api.views import api as matrix_api
from django.test import TestCase

from matrix_api.admin import MatrixAdmin
from matrix_api.forms import MatrixForm
from matrix_api.models import Matrix


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
