# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask using the Application Factory Pattern. This API allows you to manage customers, mechanics, and service tickets with full CRUD operations and mechanic assignment capabilities.

## Features

- **Customer Management**: Full CRUD operations for customers with authentication
- **Mechanic Management**: Full CRUD operations for mechanics
- **Service Ticket Management**: Create, read, update, and delete service tickets
- **Mechanic Assignment**: Assign and remove mechanics from service tickets
- **Authentication**: JWT-based login for customers with protected routes
- **Database Relationships**: Many-to-many relationships between mechanics and service tickets
- **Input Validation**: Comprehensive validation using Marshmallow schemas
- **Error Handling**: Proper error responses and status codes

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**
   ```powershell
   cd "path/to/Mechanic API"
   ```

2. **The project uses a virtual environment which should be automatically configured**

3. **Install dependencies using the virtual environment**
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Run the application**
   ```powershell
   .venv\Scripts\python.exe app.py
   ```

The API will be available at `http://127.0.0.1:5000`

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

### Create a Customer (with password)
```bash
curl -X POST http://localhost:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "password": "securepassword"
  }'
```

### Login a Customer
```bash
curl -X POST http://localhost:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@email.com",
    "password": "securepassword"
  }'
# Returns a token for authenticated requests
```

### Get My Service Tickets (Authenticated)
```bash
curl -X GET http://localhost:5000/customers/my-tickets \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Update a Customer (Authenticated)
```bash
curl -X PUT http://localhost:5000/customers/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "555-5678"
  }'
```

### Delete a Customer (Error if has tickets)
```bash
curl -X DELETE http://localhost:5000/customers/1
# Returns details of blocking tickets if any
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

### Assign Mechanic to Service Ticket
```bash
curl -X PUT http://localhost:5000/service-tickets/1/assign-mechanic/1
# Automatically sets status to 'In Progress' if 'Open'
```

### Update Service Ticket Status
```bash
curl -X PUT http://localhost:5000/service-tickets/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Completed",
    "actual_cost": 350.00
  }'
# Sets completed_at timestamp when status changes to 'Completed'
```

### Delete a Mechanic (Error if assigned)
```bash
curl -X DELETE http://localhost:5000/mechanics/1
# Returns details of assigned tickets if any
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

### Get Tickets by Customer
```bash
curl -X GET http://localhost:5000/service-tickets/customer/1
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
