from celery import shared_task
from .models import Product
from django.core.mail import send_mail

@shared_task
def generate_inventory_report():
    products = Product.objects.all()
    low_stock_items = [
        {
            "product": product.name,
            "quantity": product.quantity,
            "supplier": product.supplier.name
        } 
        for product in products if product.is_low_stock()
    ]

    # Example report content
    report_content = "Low Stock Items:\n\n"
    for item in low_stock_items:
        report_content += f"Product: {item['product']}, Quantity: {item['quantity']}, Supplier: {item['supplier']}\n"

    # Save or send the report
    send_mail(
        subject="Inventory Report",
        message=report_content,
        from_email="noreply@yourapp.com",
        recipient_list=["admin@yourapp.com"],
    )
    return "Inventory report generated and sent."
