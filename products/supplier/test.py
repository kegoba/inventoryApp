from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Supplier
from rest_framework import serializers

class SupplierViewSetTests(APITestCase):
    def setUp(self):
        self.supplier_data = {
            "first_name": "Dorcas",
            "last_name": "Irubor",
            "email": "dorcas@example.com",
        }
        self.supplier = Supplier.objects.create(**self.supplier_data)
        self.url = "/api/v1/suppliers/"

    def test_list_suppliers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("suppliers", response.data)

    def test_retrieve_supplier(self):
        response = self.client.get(f"{self.url}{self.supplier.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.supplier.first_name)
        self.assertEqual(response.data["last_name"], self.supplier.last_name)

    def test_create_supplier(self):
        new_supplier_data = {
          "first_name": "Dorcas",
            "last_name": "Irubor",
            "email": "dorcas@example.com",
        }
        response = self.client.post(self.url, new_supplier_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], new_supplier_data["first_name"])

    def test_update_supplier(self):
        updated_data = {"first_name": "Johnathan", "last_name": "Doe"}
        response = self.client.put(f"{self.url}{self.supplier.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], updated_data["first_name"])

    def test_delete_supplier(self):
        response = self.client.delete(f"{self.url}{self.supplier.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supplier_not_found(self):
        response = self.client.get(f"{self.url}99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_supplier_invalid_data(self):
        invalid_data = {"first_name": "", "last_name": "", "email": "invalidemail"}
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

