Project Overview
This project was implemented using Django Rest Framework (DRF) for managing products, inventory, and generating reports. It includes endpoints for CRUD operations on products, inventory management, and background task handling for report generation.




Setup Guide for Inventory Management System

Prerequisites
Ensure the following tools are installed on your machine:

Docker: To run containerized services.
Docker Compose: To manage multi-container Docker applications.
Git: To clone the repository.
Step 1: Clone the Repository
Open a terminal or command prompt.

Run the following command to clone the repository:

bash
Copy
Edit
git clone https://github.com/kegoba/inventoryApp.git
cd inventoryApp

Step 2: Set Up Environment Variables
Create a .env file in the root of your project and add the following variables:

plaintext
Copy
Edit
# Database URL for database connection (PostgreSQL)
DATABASE_URL= your_db_url

# Django Secret Key (change to a secret value)
SECRET_KEY = your_django_secret_key

# Celery Broker URL (if using Redis, change this)
CELERY_BROKER_URL=your_celery_broker_url
Step 3: Install Docker and Docker Compose
For Windows Users:
Install Docker Desktop:

Download Docker Desktop for Windows from here.
Follow the installation instructions.
Enable WSL 2 (Windows Subsystem for Linux 2):


For Mac Users:
Install Docker Desktop:

Download Docker Desktop for Mac from here.
Follow the installation instructions.
Install Docker Compose (bundled with Docker Desktop).

For Linux Users:
Install Docker:

Follow the installation guide for your Linux distribution from here.
Install Docker Compose:

Follow the guide for installing Docker Compose from here.

Step 4: Build the Docker Containers
In the terminal (inside your project directory), run the following command to build and start the Docker containers:

bash
Copy
Edit
docker-compose up --build
This command will build the application’s Docker images and start the services (Web, Database, Celery worker,).

Wait for services to start:

Docker will pull images (if needed) and start the containers defined in docker-compose.yml.
The web service will wait until the database is ready.


Step 5: Run Database Migrations
After the containers have started, you need to run the database migrations to set up the database schema.

Run this command:

bash
Copy
Edit
docker-compose exec web python manage.py migrate


Accessing The API 

complete postman documentation : https://documenter.getpostman.com/view/29626607/2sAYQakAxF

Access the server at base_url :  https://inventoryapp-nm6r.onrender.com/api/v1/



Accessing API Endpoints via any browser and postman
Products API
List Products:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/
Method: GET
Description: Retrieves a list of all products.

List Products:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/?page=1&per_page=10&name=Laptop
Method: GET
Description: Retrieves a list with query params products.


Retrieve Product:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/<pk>/
Method: GET
Description: Retrieves details of a specific product by its primary key (<pk>).

Create Product:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/
Method: POST
Description: Creates a new product.

Update Product:
URL:https://inventoryapp-nm6r.onrender.com/api/v1/products/<pk>/
Method: PUT/PATCH
Description: Updates an existing product by its primary key (<pk>).

Delete Product:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/<pk>/
Method: DELETE
Description: Deletes a product by its primary key (<pk>).

Upload csv file
URL : https://inventoryapp-nm6r.onrender.com/api/v1/upload/
Method  :  POST
Description: Creates bulk product.
Please include supplier_id


Inventory API
List Inventory:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/inventory/
Method: GET
Description: Retrieves a list of all inventory items.

Retrieve Inventory Item:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/inventory/<pk>/
Method: GET
Description: Retrieves details of a specific inventory item by its primary key (<pk>).

Update Inventory Item:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/inventory/<pk>/
Method: PUT/PATCH
Description: Updates an existing inventory item by its primary key (<pk>).

Low Stock Alerts:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/products/low_stock/
Method: GET
Description: Retrieves a list of inventory items with low stock.

Reports API
Generate Report:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/report/
Method: GET
Description: Initiates the generation of an inventory report.




List Suppliers:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/suppliers/
Method: GET
Description: Retrieves a list of all products.

Retrieve Supplier:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/suppliers/<pk>/
Method: GET
Description: Retrieves details of a specific product by its primary key (<pk>).

Create Supplier:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/suppliers/
Method: POST
Description: Creates a new product.

Update Supplier:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/suppliers/<pk>/
Method: PUT/PATCH
Description: Updates an existing product by its primary key (<pk>).

Delete Supplier:
URL: https://inventoryapp-nm6r.onrender.com/api/v1/suppliers/<pk>/
Method: DELETE
Description: Deletes a product by its primary key (<pk>).





To test use below command in the project root directory
python manage.py test --keepdb




--Django>=4.2.10, <5.0.0