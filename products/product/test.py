from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Supplier
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

class ProductViewSetTests(APITestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(
            "first_name": "Dorcas",
            "last_name": "Irubor",
            "email": "dorcas@example.com",
            )
        self.product_data = {
            "name": "laptop",
            "price": 10.0,
            "quantity": 100,
            "supplier_id": self.supplier.id,
        }
        self.product = Product.objects.create(**self.product_data)
        self.url = "/api/v1/products/"

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)

    def test_retrieve_product(self):
        response = self.client.get(f"{self.url}{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_create_product(self):
        new_product_data = {
            "name": "Product 2",
            "price": 15.0,
            "quantity": 200,
            "supplier_id": self.supplier.id,
        }
        response = self.client.post(self.url, new_product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], new_product_data["name"])

    def test_update_product(self):
        updated_data = {
            "name": "peak milk",
            "price": 20.0,
            "quantity": 100,
        }
        response = self.client.put(f"{self.url}{self.product.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], updated_data["name"])

    def test_delete_product(self):
        response = self.client.delete(f"{self.url}{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_low_stock(self):
        response = self.client.get(f"{self.url}low_stock/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("low_stock_products", response.data)

class UploadFileViewSetTests(APITestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        self.product_data = {
            "name": "Product 1",
            "price": 10.0,
            "quantity": 100,
            "supplier_id": self.supplier.id,
        }
        self.product = Product.objects.create(**self.product_data)
        self.url = "/api/upload-file/"

    def test_upload_file_success(self):
        file_content = "name,price,quantity,supplier_id\nProduct 1,10.0,100,1\nProduct 2,20.0,200,1"
        file = SimpleUploadedFile("test.csv", file_content.encode('utf-8'), content_type="text/csv")

        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("CSV is being processed.", response.data["message"])

    def test_upload_file_missing(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No file provided")

    @patch('products.tasks.process_csv_task')
    def test_upload_file_with_task_mock(self, mock_process_csv_task):
        mock_process_csv_task.return_value = {"message": "CSV processing completed.", "task": "mock_task_id"}

        file_content = "name,price,quantity,supplier_id\nProduct 1,10.0,100,1\nProduct 2,20.0,200,1"
        file = SimpleUploadedFile("test.csv", file_content.encode('utf-8'), content_type="text/csv")

        response = self.client.post(self.url, {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "CSV is being processed.")
        self.assertEqual(response.data["task"], "mock_task_id")
