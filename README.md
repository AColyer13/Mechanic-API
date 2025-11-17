# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask using the Application Factory Pattern. This API allows you to manage customers, mechanics, and service tickets with full CRUD operations, mechanic assignment capabilities, rate limiting, and caching.

## Features

- **Customer Management**: Full CRUD operations for customers
- **Mechanic Management**: Full CRUD operations for mechanics
- **Service Ticket Management**: Create, read, update, and delete service tickets
- **Mechanic Assignment**: Assign and remove mechanics from service tickets
- **Database Relationships**: Many-to-many relationships between mechanics and service tickets
- **Input Validation**: Comprehensive validation using Marshmallow schemas
- **Error Handling**: Proper error responses and status codes
- **Rate Limiting**: Protection against API abuse with configurable limits (Flask-Limiter)
- **Caching**: Performance optimization with in-memory caching (Flask-Caching)
- **Database Migrations**: Schema versioning with Flask-Migrate
- **MySQL Database**: Persistent data storage with MySQL
- **Interactive Client**: Command-line client for easy API testing

## Technical Stack

- **Framework**: Flask 3.0.0
- **Database**: MySQL with SQLAlchemy ORM
- **Serialization**: Marshmallow for data validation and serialization
- **Rate Limiting**: Flask-Limiter (10 requests/minute on create endpoints)
- **Caching**: Flask-Caching (5-minute cache on GET all endpoints)
- **Database Migrations**: Flask-Migrate
- **API Testing**: Custom Python client with requests library

## Rate Limiting & Caching

### Rate Limiting
The API implements rate limiting on critical endpoints to prevent abuse:
- **POST /customers/**: Limited to 10 requests per minute
- **POST /mechanics/**: Limited to 10 requests per minute
- **Global Default**: 200 requests per day, 50 requests per hour for all other routes

When rate limit is exceeded, you'll receive a `429 Too Many Requests` response.

### Caching
Performance-critical endpoints are cached to reduce database load:
- **GET /customers/**: Results cached for 5 minutes
- **GET /mechanics/**: Results cached for 5 minutes

Cache is automatically invalidated when new records are created to ensure data freshness.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**
   ```powershell
   cd "path/to/Mechanic API"
   ```

2. **Create and configure MySQL database**
   ```sql
   CREATE DATABASE mechanicshopdata;
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```properties
   FLASK_ENV=development
   SECRET_KEY=dev-secret-key-change-in-production
   DATABASE_URL=mysql+mysqlconnector://root:password@localhost/mechanicshopdata
   DEBUG=True
   ```

4. **Install dependencies using the virtual environment**
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. **Run the application**
   ```powershell
   .venv\Scripts\python.exe app.py
   ```

The API will be available at `http://127.0.0.1:5000`

## Using the Interactive Client

The project includes an interactive command-line client for easy API testing:

```powershell
.venv\Scripts\python.exe client.py
```

The client provides:
- **Menu-driven interface** for all API operations
- **Automated test suite** to create sample data
- **Input validation** and error handling
- **Formatted JSON responses**

### Client Features
- Create, read, update, and delete customers, mechanics, and service tickets
- Assign/remove mechanics from service tickets
- Query tickets by customer or mechanic
- Run complete automated test suite (creates sample data and tests all endpoints)

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
- **Data Validation**: Comprehensive input validation using Marshmallow schemas
- **Modular Architecture**: Clean separation using Flask blueprints

## Project Structure

```
/project
├── /application
│   ├── __init__.py                 # Application factory with create_app()
│   ├── extensions.py              # Flask extensions initialization
│   ├── models.py                  # Database models
│   └── /blueprints
│       ├── /customer
│       │   ├── __init__.py        # Customer blueprint initialization
│       │   ├── routes.py          # Customer CRUD routes
│       │   └── customerSchemas.py # Customer Marshmallow schemas
│       ├── /mechanic
│       │   ├── __init__.py        # Mechanic blueprint initialization
│       │   ├── routes.py          # Mechanic CRUD routes
│       │   └── schemas.py         # Mechanic Marshmallow schemas
│       └── /service_ticket
│           ├── __init__.py        # Service ticket blueprint initialization
│           ├── routes.py          # Service ticket routes
│           └── schemas.py         # Service ticket Marshmallow schemas
├── app.py                         # Main application entry point
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
└── .env.example                   # Environment variables template
```

## Setup Instructions

1. **Clone or download the project**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   copy .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Customers (`/customers`)

- `POST /customers/` - Create a new customer
- `GET /customers/` - Get all customers
- `GET /customers/<id>` - Get a specific customer
- `PUT /customers/<id>` - Update a customer
- `DELETE /customers/<id>` - Delete a customer

### Mechanics (`/mechanics`)

- `POST /mechanics/` - Create a new mechanic
- `GET /mechanics/` - Get all mechanics
- `GET /mechanics/<id>` - Get a specific mechanic
- `PUT /mechanics/<id>` - Update a mechanic
- `DELETE /mechanics/<id>` - Delete a mechanic

### Service Tickets (`/service-tickets`)

- `POST /service-tickets/` - Create a new service ticket
- `GET /service-tickets/` - Get all service tickets
- `GET /service-tickets/<id>` - Get a specific service ticket
- `PUT /service-tickets/<id>` - Update a service ticket
- `DELETE /service-tickets/<id>` - Delete a service ticket
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign mechanic to ticket
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic from ticket
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
   - Create Customer
   - Get All Customers
   - Get Customer by ID
   - Update Customer
   - Delete Customer

2. **Mechanics Collection**
   - Create Mechanic
   - Get All Mechanics
   - Get Mechanic by ID
   - Update Mechanic
   - Delete Mechanic

3. **Service Tickets Collection**
   - Create Service Ticket
   - Get All Service Tickets
   - Get Service Ticket by ID
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
- The application follows the Application Factory pattern for better testability and modularity
- Each blueprint is self-contained with its own routes and schemas
