# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask using the Application Factory Pattern. This API allows you to manage customers, mechanics, and service tickets with full CRUD operations and mechanic assignment capabilities.

## Features

- **Customer Management**: Full CRUD operations for customers
- **Mechanic Management**: Full CRUD operations for mechanics
- **Service Ticket Management**: Create, read, update, and delete service tickets
- **Mechanic Assignment**: Assign and remove mechanics from service tickets
- **Database Relationships**: Many-to-many relationships between mechanics and service tickets
- **Input Validation**: Comprehensive validation using Marshmallow schemas
- **Error Handling**: Proper error responses and status codes
- **Rate Limiting**: Protection against API abuse with Flask-Limiter
- **Caching**: Performance optimization with Flask-Caching for frequently accessed data
- **Data Validation**: Comprehensive input validation using Marshmallow schemas
- **Modular Architecture**: Clean separation using Flask blueprints

## Project Structure

```
/Mechanic API - Copy
├── /application
│   ├── __init__.py                 # Application factory with create_app()
│   ├── extensions.py              # Flask extensions initialization (SQLAlchemy, Marshmallow, Migrate, Limiter, Cache)
│   ├── models.py                  # Database models
│   └── /blueprints
│       ├── /customer
│       │   ├── __init__.py        # Customer blueprint initialization
│       │   ├── routes.py          # Customer CRUD routes (with rate limiting & caching)
│       │   └── customerSchemas.py # Customer Marshmallow schemas
│       ├── /mechanic
│       │   ├── __init__.py        # Mechanic blueprint initialization
│       │   ├── routes.py          # Mechanic CRUD routes (with rate limiting & caching)
│       │   └── schemas.py         # Mechanic Marshmallow schemas
│       └── /service_ticket
│           ├── __init__.py        # Service ticket blueprint initialization
│           ├── routes.py          # Service ticket routes (with rate limiting & caching)
│           └── schemas.py         # Service ticket Marshmallow schemas
├── app.py                         # Main application entry point
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies (includes Flask-Limiter & Flask-Caching)
├── README.md                      # Project documentation
└── .env.example                   # Environment variables template
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

4. **Set up environment variables (optional)**
   ```powershell
   copy .env.example .env
   # Edit .env file with your configuration
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

### Service Tickets (`/service-tickets`)

- `POST /service-tickets/` - Create a new service ticket *(Rate Limited: 20/hour)*
- `GET /service-tickets/` - Get all service tickets
- `GET /service-tickets/<id>` - Get a specific service ticket *(Cached: 3 minutes)*
- `PUT /service-tickets/<id>` - Update a service ticket
- `DELETE /service-tickets/<id>` - Delete a service ticket
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign mechanic to ticket
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic from ticket
- `PUT /service-tickets/<ticket_id>/edit` - **NEW**: Bulk add/remove mechanics from ticket
- `GET /service-tickets/customer/<customer_id>` - Get all tickets for a customer
- `GET /service-tickets/mechanic/<mechanic_id>` - Get all tickets for a mechanic

### Mechanics (`/mechanics`)

- `POST /mechanics/` - Create a new mechanic *(Rate Limited: 5/hour)*
- `GET /mechanics/` - Get all mechanics *(Cached: 5 minutes)*
- `GET /mechanics/<id>` - Get a specific mechanic
- `PUT /mechanics/<id>` - Update a mechanic
- `DELETE /mechanics/<id>` - Delete a mechanic
- `GET /mechanics/by-workload` - **NEW**: Get mechanics ordered by ticket count

### Customers (`/customers`)

- `POST /customers/` - Create a new customer *(Rate Limited: 10/hour)*
- `GET /customers/` - Get all customers *(Cached: 10 minutes)* **[Now with Pagination]**
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer
- `DELETE /customers/<id>` - Delete a customer

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

### Assign Mechanic to Service Ticket
```bash
curl -X PUT http://localhost:5000/service-tickets/1/assign-mechanic/1
```

## New API Usage Examples

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

## Database Models

### Customer
- `id`: Primary key
- `first_name`: Customer's first name (required)
- `last_name`: Customer's last name (required)
- `email`: Customer's email (required, unique)
- `phone`: Customer's phone number
- `address`: Customer's address
- `created_at`: Timestamp of creation

### Mechanic
- `id`: Primary key
- `first_name`: Mechanic's first name (required)
- `last_name`: Mechanic's last name (required)
- `email`: Mechanic's email (required, unique)
- `phone`: Mechanic's phone number
- `specialty`: Mechanic's area of expertise
- `hourly_rate`: Mechanic's hourly billing rate
- `hire_date`: Date mechanic was hired
- `created_at`: Timestamp of creation

### ServiceTicket
- `id`: Primary key
- `customer_id`: Foreign key to Customer (required)
- `vehicle_year`: Year of the vehicle
- `vehicle_make`: Make of the vehicle
- `vehicle_model`: Model of the vehicle
- `vehicle_vin`: Vehicle identification number
- `description`: Description of work needed (required)
- `estimated_cost`: Estimated cost of repairs
- `actual_cost`: Actual cost of repairs
- `status`: Ticket status (Open, In Progress, Completed, Cancelled)
- `created_at`: Timestamp of creation
- `completed_at`: Timestamp when completed

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

## Development Notes

- The API uses SQLAlchemy for database operations
- Marshmallow provides serialization and validation
- Flask-Migrate can be used for database migrations
- Flask-Limiter provides rate limiting protection
- Flask-Caching improves performance with in-memory caching
- The application follows the Application Factory pattern for better testability and modularity
- Each blueprint is self-contained with its own routes and schemas
- Rate limiting is implemented per IP address using `get_remote_address`
- Caching uses SimpleCache (in-memory) for development; consider Redis for production
