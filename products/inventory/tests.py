from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Supplier
from .repositories import InventoryRepository
from unittest.mock import patch
from django.urls import reverse

class InventoryViewSetTests(APITestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            first_name= "Dorcas",
            last_name ="Irubor",
            email = "dorcas@example.com",)
        self.product = Product.objects.create(
            name="chair",
            price=50.0,
            quantity=100,
            supplier=self.supplier
        )
        self.url = "/api/v1/inventory/"
    def test_list_inventory(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.product.name)

    def test_retrieve_inventory_item(self):
        response = self.client.get(f"{self.url}{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_inventory(self):
        updated_data = {
            "quantity": 150,
        }
        response = self.client.put(f"{self.url}{self.product.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], updated_data["quantity"])

    def test_low_stock_alert(self):
        response = self.client.get(f"{self.url}low_stock/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("low_stock_alert", response.data)


class ReportViewSetTests(APITestCase):

    @patch('inventory.views.generate_report')
    def test_generate_report_success(self, mock_generate_report):
        mock_generate_report.return_value = {
            "low_stock_alerts": [],
            "supplier_performance": []
        }

        url = reverse('/api/v1/report/') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Report generated successfully")
        self.assertEqual(response.data["data"]["low_stock_alerts"], [])
        self.assertEqual(response.data["data"]["supplier_performance"], [])

    @patch('inventory.views.generate_report')
    def test_generate_report_failure(self, mock_generate_report):
        mock_generate_report.side_effect = Exception("Report generation failed")

        url = reverse('/api/v1/report/')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "An error occurred while generating the report")
        self.assertIn("details", response.data)
        self.assertEqual(response.data["details"], "Report generation failed")

