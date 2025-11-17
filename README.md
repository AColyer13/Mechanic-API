# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask using the Application Factory Pattern. This API allows you to manage customers, mechanics, and service tickets with full CRUD operations and mechanic assignment capabilities.

## Features

- **Customer Management**: Full CRUD operations for customers with authentication
- **Mechanic Management**: Full CRUD operations for mechanics
- **Inventory Management**: Full CRUD operations for inventory parts and supplies
- **Service Ticket Management**: Create, read, update, and delete service tickets
- **Mechanic Assignment**: Assign and remove mechanics from service tickets
- **Inventory Tracking**: Associate inventory parts with service tickets
- **Database Relationships**: Many-to-many relationships between mechanics/service tickets and inventory/service tickets
- **Input Validation**: Comprehensive validation using Marshmallow schemas with custom validations
- **Error Handling**: Proper error responses and status codes
- **Rate Limiting**: Protection against API abuse with Flask-Limiter
- **Caching**: Performance optimization with Flask-Caching for frequently accessed data
- **Authentication**: Token-based authentication system
- **Modular Architecture**: Clean separation using Flask blueprints with Application Factory pattern

## Project Structure

```
/Mechanic API - Copy
├── /application
│   ├── __init__.py                 # Application factory with create_app()
│   ├── extensions.py              # Flask extensions initialization (SQLAlchemy, Marshmallow, Migrate, Limiter, Cache)
│   ├── models.py                  # Complete database models (Customer, Mechanic, Inventory, ServiceTicket)
│   └── /blueprints
│       ├── /customer
│       │   ├── __init__.py        # Customer blueprint initialization
│       │   ├── routes.py          # Customer CRUD routes (with rate limiting & caching)
│       │   └── customerSchemas.py # Customer Marshmallow schemas with validation
│       ├── /mechanic
│       │   ├── __init__.py        # Mechanic blueprint initialization
│       │   ├── routes.py          # Mechanic CRUD routes (with rate limiting & caching)
│       │   └── schemas.py         # Mechanic Marshmallow schemas with validation
│       ├── /inventory
│       │   ├── __init__.py        # Inventory blueprint initialization
│       │   ├── routes.py          # Inventory CRUD routes
│       │   └── schemas.py         # Inventory Marshmallow schemas with validation
│       ├── /service_ticket
│       │   ├── __init__.py        # Service ticket blueprint initialization
│       │   ├── routes.py          # Service ticket routes (with rate limiting & caching)
│       │   └── schemas.py         # Service ticket Marshmallow schemas with validation
│       └── /orders
│           └── routes.py          # Orders routes
├── /utils
│   └── auth.py                    # Authentication utilities
├── app.py                         # Main application entry point
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies (includes Flask-Limiter & Flask-Caching)
├── README.md                      # Project documentation
└── .env                           # Environment variables (configure your database here)
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**
   ```powershell
   cd "c:\Users\adamc\OneDrive\Coding Temple\Mechanic API - Copy"
   ```

2. **Create a virtual environment (if not already created)**
   ```powershell
   python -m venv .venv
   ```

3. **Install dependencies using the virtual environment**
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   
   **Required packages include:**
   - Flask
   - Flask-SQLAlchemy
   - Flask-Marshmallow
   - Flask-Migrate
   - Flask-Limiter
   - Flask-Caching
   - marshmallow-sqlalchemy

4. **Set up environment variables**
   ```powershell
   # Create .env file with your database configuration
   # Example for MySQL:
   # DATABASE_URL=mysql+mysqlconnector://root:password@localhost/mechanicshopdata
   # 
   # Or use SQLite for development:
   # DATABASE_URL=sqlite:///mechanic_shop.db
   ```

5. **Run the application**
   ```powershell
   .venv\Scripts\python.exe app.py
   ```

The API will be available at `http://127.0.0.1:5000`

## Rate Limiting and Caching

### Rate Limiting
The API implements rate limiting to protect against abuse and ensure fair usage:

- **Customer Registration**: Limited to 10 registrations per hour per IP address
  - Prevents spam customer creation and automated bot registrations
- **Mechanic Registration**: Limited to 5 registrations per hour per IP address  
  - Protects against fake mechanic registrations and system abuse
- **Service Ticket Creation**: Limited to 20 tickets per hour per IP address
  - Prevents order spam and ensures legitimate usage of the ticketing system

### Caching
The API uses caching to improve performance and reduce database load:

- **Customer List**: Cached for 10 minutes
  - Reduces database queries for frequently accessed customer data in admin panels
- **Mechanic List**: Cached for 5 minutes
  - Improves performance since mechanic lists don't change frequently
- **Individual Service Tickets**: Cached for 3 minutes
  - Speeds up ticket detail retrieval for status checks and updates

When rate limits are exceeded, the API returns a `429 Too Many Requests` response. Cached responses improve response times significantly for frequently accessed endpoints.

## Resolving Common Issues

### "pip is not recognized" Error
If you see this error, use the full path to the Python executable:
```powershell
.venv\Scripts\python.exe -m pip install [package-name]
```

### PowerShell Execution Policy
If you can't activate the virtual environment due to execution policy, use the Python executable directly:
```powershell
.venv\Scripts\python.exe app.py
```

### Installing Flask-Limiter and Flask-Caching
If these packages are missing, install them manually:
```powershell
.venv\Scripts\python.exe -m pip install Flask-Limiter Flask-Caching
```

## API Endpoints

### Customers (`/customers`)

- `POST /customers/` - Create a new customer *(Rate Limited: 10/hour)*
- `GET /customers/` - Get all customers *(Cached: 10 minutes)* **[With Pagination]**
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer
- `DELETE /customers/<id>` - Delete a customer
- `POST /customers/login` - Customer authentication *(Rate Limited: 5/minute)*

### Mechanics (`/mechanics`)

- `POST /mechanics/` - Create a new mechanic *(Rate Limited: 5/hour)*
- `GET /mechanics/` - Get all mechanics *(Cached: 5 minutes)*
- `GET /mechanics/<id>` - Get a specific mechanic
- `PUT /mechanics/<id>` - Update a mechanic
- `DELETE /mechanics/<id>` - Delete a mechanic
- `GET /mechanics/by-workload` - Get mechanics ordered by ticket count

### Inventory (`/inventory`)

- `POST /inventory/` - Create a new inventory item *(Token Required)*
- `GET /inventory/` - Get all inventory items
- `GET /inventory/<id>` - Get a specific inventory item
- `PUT /inventory/<id>` - Update an inventory item *(Token Required)*
- `DELETE /inventory/<id>` - Delete an inventory item *(Token Required)*

### Service Tickets (`/service-tickets`)

- `POST /service-tickets/` - Create a new service ticket *(Rate Limited: 20/hour)*
- `GET /service-tickets/` - Get all service tickets
- `GET /service-tickets/<id>` - Get a specific service ticket *(Cached: 3 minutes)*
- `PUT /service-tickets/<id>` - Update a service ticket
- `DELETE /service-tickets/<id>` - Delete a service ticket
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign mechanic to ticket
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic from ticket
- `PUT /service-tickets/<ticket_id>/edit` - Bulk add/remove mechanics from ticket
- `GET /service-tickets/customer/<customer_id>` - Get all tickets for a customer
- `GET /service-tickets/mechanic/<mechanic_id>` - Get all tickets for a mechanic

## Sample API Usage

### Create a Customer
```bash
curl -X POST http://localhost:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "555-1234",
    "address": "123 Main St"
  }'
```

### Create a Mechanic
```bash
curl -X POST http://localhost:5000/mechanics/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Mike",
    "last_name": "Smith",
    "email": "mike.smith@shop.com",
    "phone": "555-5678",
    "specialty": "Engine Repair",
    "hourly_rate": 85.00,
    "hire_date": "2023-01-15"
  }'
```

### Create an Inventory Item
```bash
curl -X POST http://localhost:5000/inventory/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Brake Pads",
    "price": 45.99
  }'
```

### Create a Service Ticket
```bash
curl -X POST http://localhost:5000/service-tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "vehicle_year": 2020,
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_vin": "1HGBH41JXMN109186",
    "description": "Oil change and brake inspection",
    "estimated_cost": 150.00
  }'
```

### Customer Login
```bash
curl -X POST http://localhost:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@email.com",
    "password": "your_password"
  }'
```

### Assign Mechanic to Service Ticket
```bash
curl -X PUT http://localhost:5000/service-tickets/1/assign-mechanic/1
```

## Advanced API Usage Examples

### Bulk Update Mechanics on Service Ticket
```bash
curl -X PUT http://localhost:5000/service-tickets/1/edit \
  -H "Content-Type: application/json" \
  -d '{
    "add_ids": [1, 2, 3],
    "remove_ids": [4, 5]
  }'
```

### Get Mechanics by Workload
```bash
curl -X GET http://localhost:5000/mechanics/by-workload
```

### Get Customers with Pagination
```bash
# Get first page (10 customers per page by default)
curl -X GET http://localhost:5000/customers/

# Get specific page with custom page size
curl -X GET "http://localhost:5000/customers/?page=2&per_page=5"
```

### Get All Inventory Items
```bash
curl -X GET http://localhost:5000/inventory/
```

## Database Models

### Customer
- `id`: Primary key
- `first_name`: Customer's first name (required, 1-50 chars)
- `last_name`: Customer's last name (required, 1-50 chars)
- `email`: Customer's email (required, unique, valid email format)
- `phone`: Customer's phone number (max 20 chars)
- `address`: Customer's address (max 200 chars)
- `created_at`: Timestamp of creation

### Mechanic
- `id`: Primary key
- `first_name`: Mechanic's first name (required, 1-50 chars)
- `last_name`: Mechanic's last name (required, 1-50 chars)
- `email`: Mechanic's email (required, unique, valid email format)
- `phone`: Mechanic's phone number (max 20 chars)
- `specialty`: Mechanic's area of expertise (max 100 chars)
- `hourly_rate`: Mechanic's hourly billing rate (min 0)
- `hire_date`: Date mechanic was hired
- `created_at`: Timestamp of creation

### Inventory
- `id`: Primary key
- `name`: Part/supply name (required, 1-100 chars)
- `price`: Part/supply price (required, min 0)
- `created_at`: Timestamp of creation

### ServiceTicket
- `id`: Primary key
- `customer_id`: Foreign key to Customer (required)
- `vehicle_year`: Year of the vehicle (1900-2050)
- `vehicle_make`: Make of the vehicle (max 50 chars)
- `vehicle_model`: Model of the vehicle (max 50 chars)
- `vehicle_vin`: Vehicle identification number (max 17 chars)
- `description`: Description of work needed (required, min 1 char)
- `estimated_cost`: Estimated cost of repairs (min 0)
- `actual_cost`: Actual cost of repairs (min 0)
- `status`: Ticket status (Open, In Progress, Completed, Cancelled)
- `created_at`: Timestamp of creation
- `completed_at`: Timestamp when completed (auto-set when status = Completed)

### Relationships
- **Many-to-Many**: ServiceTicket ↔ Mechanic (service_ticket_mechanics table)
- **Many-to-Many**: ServiceTicket ↔ Inventory (service_ticket_inventory table)
- **One-to-Many**: Customer → ServiceTicket

## Testing with Postman

Import the following collection structure in Postman:

1. **Customers Collection**
   - Create Customer *(Test rate limiting by making 11+ requests within an hour)*
   - Get All Customers *(Test caching by making multiple requests)*
   - Get Customer by ID
   - Update Customer
   - Delete Customer

2. **Mechanics Collection**
   - Create Mechanic *(Test rate limiting by making 6+ requests within an hour)*
   - Get All Mechanics *(Test caching by making multiple requests)*
   - Get Mechanic by ID
   - Update Mechanic
   - Delete Mechanic

3. **Service Tickets Collection**
   - Create Service Ticket *(Test rate limiting by making 21+ requests within an hour)*
   - Get All Service Tickets
   - Get Service Ticket by ID *(Test caching by making multiple requests)*
   - Update Service Ticket
   - Delete Service Ticket
   - Assign Mechanic to Ticket
   - Remove Mechanic from Ticket
   - Get Customer Tickets
   - Get Mechanic Tickets

## Architecture & Development Notes

### Clean Architecture
- **Application Factory Pattern**: Modular Flask app creation with `create_app()`
- **Blueprint Organization**: Each feature (customer, mechanic, inventory, service_ticket) is self-contained
- **Schema Validation**: Comprehensive Marshmallow schemas with custom validations and error handling
- **No Duplicate Code**: Eliminated duplicate models, schemas, and blueprint files

### Technology Stack
- **Flask & Extensions**: SQLAlchemy (ORM), Marshmallow (serialization), Flask-Migrate (migrations)
- **Performance**: Flask-Limiter (rate limiting), Flask-Caching (caching), proper database relationships
- **Security**: Token-based authentication, input validation, SQL injection protection
- **Database**: Supports MySQL (production) and SQLite (development)

### Key Features
- **Rate Limiting**: Per-IP limits prevent API abuse
- **Caching**: In-memory caching improves response times (consider Redis for production)
- **Validation**: Comprehensive input validation with custom field validators
- **Error Handling**: Proper HTTP status codes and error messages
- **Database Design**: Efficient many-to-many relationships with association tables

### Project Cleanup Completed
- ✅ Removed duplicate root `schemas.py`, `models.py`, and `blueprints/` folder
- ✅ Consolidated all schemas into their respective blueprint modules
- ✅ Fixed conflicting blueprint registrations
- ✅ Maintained single source of truth for all components
