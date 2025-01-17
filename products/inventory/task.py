from celery import shared_task
import os, csv
from datetime import datetime
from django.db.models import Sum, F


from io import StringIO
from django.db import transaction


# self defined
from products.models import Product,Supplier
from ..product.serializers import ProductSerializer
from ..product.repositories import ProductRepository






#@shared_task
def generate_report():
    report_data = {
        "low_stock_alerts": [],
        "supplier_performance": []
    }

    # Fetch products with low stock
    low_stock_products = Product.objects.filter(quantity__lte=10)
    for product in low_stock_products:
        # Access supplier's name using the correct foreign key relationship
        supplier_name = f"{product.supplier_id.first_name} {product.supplier_id.last_name}" if product.supplier_id else "Unknown"
        report_data["low_stock_alerts"].append({
            "product_name": product.name,
            "quantity": product.quantity,
            "supplier_name": supplier_name
        })

    # Fetch supplier performance
    supplier_performance = (
        Product.objects.values("supplier_id__first_name", "supplier_id__last_name")
        .annotate(
            total_products=Sum("quantity"),
            total_value=Sum(F("quantity") * F("price"))
        )
        .order_by("-total_value")
    )
    for supplier in supplier_performance:
        supplier_name = f"{supplier['supplier_id__first_name']} {supplier['supplier_id__last_name']}"
        report_data["supplier_performance"].append({
            "supplier_name": supplier_name,
            "total_products": supplier["total_products"],
            "total_value": supplier["total_value"]
        })

    # Generate CSV report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"inventory_report_{timestamp}.csv"
    file_path = os.path.join("reports", report_file)

    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)

    # Write report data to CSV file
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write low stock alerts section
        writer.writerow(["Low Stock Alerts"])
        writer.writerow(["Product Name", "Quantity", "Supplier Name"])
        for item in report_data["low_stock_alerts"]:
            writer.writerow([item["product_name"], item["quantity"], item["supplier_name"]])

        # Write supplier performance metrics section
        writer.writerow([])
        writer.writerow(["Supplier Performance Metrics"])
        writer.writerow(["Supplier Name", "Total Products", "Total Value"])
        for item in report_data["supplier_performance"]:
            writer.writerow([item["supplier_name"], item["total_products"], item["total_value"]])

    return {"file_path": file_path, "message": "Report generation completed successfully."}