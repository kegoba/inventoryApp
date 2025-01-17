from celery import shared_task
import os, csv
from datetime import datetime
from django.db.models import Sum, F


from io import StringIO
from django.db import transaction


# self defined
from products.models import Product,Supplier
from .serializers import ProductSerializer
from .repositories import ProductRepository



#@shared_task
def process_csv_task(file):
    file_data = file.read().decode('utf-8')
    csv_data = StringIO(file_data)
    errors = []
    success_count = 0
    line_number = 1
    csv_reader = csv.DictReader(csv_data)
    with transaction.atomic():
        for row in csv_reader:
            line_number += 1
            try:
                name = row.get('name')
                description = row.get('description', '')
                price = row.get('price', 0)
                quantity = row.get('quantity', 0)
                supplier_id = row.get('supplier_id', 0)
                try:
                    price = float(price)
                    quantity = int(quantity)
                    supplier_id = int(float(supplier_id))  
                except ValueError as e:
                    errors.append(
                        {"line": line_number, "error": f"Invalid numeric value: {e}", "row": row}
                    )
                    continue

                if not name or price < 0 or quantity < 0:
                    errors.append(
                        {"line": line_number, "error": "Invalid data in row (price/quantity)", "row": row}
                    )
                    continue
                try:
                    supplier = Supplier.objects.get(id=supplier_id)
                except Supplier.DoesNotExist:
                    errors.append(
                        {"line": line_number, "error": f"Supplier with ID {supplier_id} does not exist.", "row": row}
                    )
                    continue
                Product.objects.update_or_create(
                    name=name.strip(),
                    defaults={
                        "description": description.strip(),
                        "price": price,
                        "quantity": quantity,
                        "supplier_id": supplier,
                    },
                )
                success_count += 1
            except Exception as e:
                errors.append(
                    {"line": line_number, "error": f"Unexpected error: {str(e)}", "row": row}
                )

    return {
        "message": "CSV processing completed.",
        "records_processed": line_number - 1,
        "success_count": success_count,
        "errors": errors,
    }





#@shared_task
def generate_report():
    report_data = {
        "low_stock_alerts": [],
        "supplier_performance": []
    }

    low_stock_products = Product.objects.filter(quantity__lte=10)
    for product in low_stock_products:
        report_data["low_stock_alerts"].append({
            "product_name": product.name,
            "quantity": product.quantity,
            "supplier": product.supplier.name if product.supplier else "Unknown"
        })

    supplier_performance = (
        Product.objects.values("supplier__name")
        .annotate(
            total_products=Sum("quantity"),
            total_value=Sum(F("quantity") * F("price"))
        )
        .order_by("-total_value")
    )
    for supplier in supplier_performance:
        report_data["supplier_performance"].append({
            "supplier_name": supplier["supplier__name"],
            "total_products": supplier["total_products"],
            "total_value": supplier["total_value"]
        })

    #convert report to csv file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"inventory_report_{timestamp}.csv"
    file_path = os.path.join("reports", report_file)

    os.makedirs("reports", exist_ok=True)
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Low Stock Alerts"])
        writer.writerow(["Product Name", "Quantity", "Supplier"])
        for item in report_data["low_stock_alerts"]:
            writer.writerow([item["product_name"], item["quantity"], item["supplier"]])

        writer.writerow([])
        writer.writerow(["Supplier Performance Metrics"])
        writer.writerow(["Supplier Name", "Total Products", "Total Value"])
        for item in report_data["supplier_performance"]:
            writer.writerow([item["supplier_name"], item["total_products"], item["total_value"]])

    return {"file_path": file_path, "message": "Report generation completed successfully."}
