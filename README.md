# Mechanic Shop API

A comprehensive RESTful API for managing a mechanic shop built with Flask using the Application Factory Pattern. This API provides full CRUD operations for customers, mechanics, service tickets, and inventory parts, along with advanced features like JWT authentication, rate limiting, and caching.

## Features

### Core Functionality
- **Customer Management**: Full CRUD operations with secure password hashing (bcrypt)
- **Mechanic Management**: Complete mechanic lifecycle management
- **Service Ticket Management**: Track repairs with customer and mechanic assignments
- **Inventory Management**: Manage parts with pricing and usage tracking
- **Many-to-Many Relationships**: 
  - Mechanics ↔ Service Tickets
  - Inventory Parts ↔ Service Tickets

### Security & Authentication
- **JWT Token Authentication**: Secure customer authentication using python-jose
- **Password Hashing**: Bcrypt encryption for customer passwords
- **Token-Protected Routes**: Secured endpoints requiring Bearer token authorization
- **Customer-Specific Access**: Users can only access/modify their own data

### Performance & Protection
- **Rate Limiting**: Flask-Limiter protection against API abuse
- **Caching**: Flask-Caching for optimized database performance
- **Input Validation**: Comprehensive validation using Marshmallow schemas
- **Error Handling**: Proper error responses and status codes

## Technical Stack

- **Framework**: Flask 3.0.0
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT tokens (python-jose)
- **Password Security**: bcrypt (via passlib)
- **Serialization**: Marshmallow & marshmallow-sqlalchemy
- **Rate Limiting**: Flask-Limiter (configurable per endpoint)
- **Caching**: Flask-Caching (in-memory with 5-minute TTL)
- **Database Migrations**: Flask-Migrate with Alembic
- **API Testing**: Postman collection with 40+ requests

## Advanced Features

### JWT Token Authentication
Secure authentication system for customer accounts:

**Login Flow:**
1. Customer registers: `POST /customers/` with email and password
2. Customer logs in: `POST /customers/login` → receives JWT token
3. Protected routes require: `Authorization: Bearer <token>` header

**Protected Endpoints:**
- `GET /customers/my-tickets` - Get authenticated customer's tickets
- `PUT /customers/{id}` - Update own account only
- `DELETE /customers/{id}` - Delete own account only

**Token Features:**
- 24-hour expiration
- HS256 algorithm
- Customer ID embedded in payload
- Automatic validation via `@token_required` decorator

### Rate Limiting
Protection against API abuse with configurable limits:
- **POST /customers/**: 10 requests/minute
- **POST /mechanics/**: 10 requests/minute
- **POST /inventory/**: 20 requests/minute
- **Global Default**: 200 requests/day, 50 requests/hour

Exceeding limits returns `429 Too Many Requests` with retry-after header.

### Caching
Performance optimization with automatic invalidation:
- **GET /customers/**: 5-minute cache
- **GET /mechanics/**: 5-minute cache
- **GET /inventory/**: 5-minute cache

Cache auto-clears on create/update/delete operations for data consistency.

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
│   ├── __init__.py                      # Application factory with create_app()
│   ├── extensions.py                   # Extensions: db, cache, limiter, JWT functions
│   ├── models.py                       # Models: Customer, Mechanic, ServiceTicket, Inventory
│   └── /blueprints
│       ├── /customer
│       │   ├── __init__.py             # Customer blueprint
│       │   ├── routes.py               # CRUD + login + token-protected routes
│       │   └── customerSchemas.py      # Customer & Login schemas
│       ├── /mechanic
│       │   ├── __init__.py             # Mechanic blueprint
│       │   ├── routes.py               # CRUD operations
│       │   └── schemas.py              # Mechanic schemas
│       ├── /service_ticket
│       │   ├── __init__.py             # Service ticket blueprint
│       │   ├── routes.py               # CRUD + mechanic assignment + add parts
│       │   └── schemas.py              # Service ticket schemas
│       └── /inventory
│           ├── __init__.py             # Inventory blueprint
│           ├── routes.py               # CRUD operations
│           └── schemas.py              # Inventory schemas
├── app.py                              # Application entry point
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
├── client.py                           # Interactive CLI client
├── test_api.py                         # Automated test script
├── Mechanic API.postman_collection.json # Postman collection (40+ requests)
└── TESTING_GUIDE.md                    # Comprehensive testing documentation
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

### Authentication (`/customers`)
- `POST /customers/login` - Login and receive JWT token
- `GET /customers/my-tickets` - Get authenticated customer's tickets (requires token)

### Customers (`/customers`)
- `POST /customers/` - Create new customer (includes password hashing) [Rate Limited: 10/min]
- `GET /customers/` - Get all customers [Cached: 5 min]
- `GET /customers/<id>` - Get specific customer
- `PUT /customers/<id>` - Update customer (requires token, own account only)
- `DELETE /customers/<id>` - Delete customer (requires token, own account only)

### Mechanics (`/mechanics`)
- `POST /mechanics/` - Create new mechanic [Rate Limited: 10/min]
- `GET /mechanics/` - Get all mechanics [Cached: 5 min]
- `GET /mechanics/<id>` - Get specific mechanic
- `PUT /mechanics/<id>` - Update mechanic
- `DELETE /mechanics/<id>` - Delete mechanic

### Service Tickets (`/service-tickets`)
- `POST /service-tickets/` - Create new service ticket
- `GET /service-tickets/` - Get all service tickets
- `GET /service-tickets/<id>` - Get specific service ticket
- `PUT /service-tickets/<id>` - Update service ticket
- `DELETE /service-tickets/<id>` - Delete service ticket
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign mechanic
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove mechanic
- `PUT /service-tickets/<ticket_id>/add-part/<inventory_id>` - Add inventory part
- `GET /service-tickets/customer/<customer_id>` - Get customer's tickets
- `GET /service-tickets/mechanic/<mechanic_id>` - Get mechanic's tickets

### Inventory (`/inventory`)
- `POST /inventory/` - Create new inventory part [Rate Limited: 20/min]
- `GET /inventory/` - Get all inventory parts [Cached: 5 min]
- `GET /inventory/<id>` - Get specific inventory part
- `PUT /inventory/<id>` - Update inventory part
- `DELETE /inventory/<id>` - Delete inventory part

## Sample API Usage

### Authentication Flow

#### 1. Create a Customer (with password)
```bash
curl -X POST http://localhost:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "password": "securepassword123",
    "phone": "555-1234",
    "address": "123 Main St"
  }'
```

#### 2. Login and Get JWT Token
```bash
curl -X POST http://localhost:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@email.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "customer": { ... }
}
```

#### 3. Access Protected Route
```bash
curl -X GET http://localhost:5000/customers/my-tickets \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
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

### Create Inventory Part
```bash
curl -X POST http://localhost:5000/inventory/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Oil Filter",
    "price": 12.99
  }'
```

### Add Part to Service Ticket
```bash
curl -X PUT http://localhost:5000/service-tickets/1/add-part/1
```

## Database Models

### Customer
- `id`: Primary key
- `first_name`: Customer's first name (required)
- `last_name`: Customer's last name (required)
- `email`: Customer's email (required, unique)
- `password`: Hashed password (required, bcrypt)
- `phone`: Customer's phone number
- `address`: Customer's address
- `created_at`: Timestamp of creation
- **Relationship**: One-to-Many with ServiceTicket

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
- **Relationship**: Many-to-Many with ServiceTicket

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
- **Relationships**: 
  - Many-to-One with Customer
  - Many-to-Many with Mechanic
  - Many-to-Many with Inventory

### Inventory
- `id`: Primary key
- `name`: Part name (required, max 100 chars)
- `price`: Part price (required, must be >= 0)
- **Relationship**: Many-to-Many with ServiceTicket

## Testing with Postman

### Importing the Collection
1. Open Postman
2. Click **Import** → Select `Mechanic API.postman_collection.json`
3. Collection includes 40+ organized requests

### Collection Structure

**1. API Root**
- Get API welcome message

**2. Customers** (Full CRUD)
- Create, Read, Update, Delete operations

**3. Mechanics** (Full CRUD)
- Create, Read, Update, Delete operations

**4. Service Tickets** (Full CRUD + Assignment)
- CRUD operations
- Assign/Remove Mechanic
- Add Part to Ticket
- Query by Customer/Mechanic

**5. Authentication** ⭐
- Customer Login (auto-saves token to environment)
- Get My Tickets (requires token)
- Update Customer (requires token)
- Delete Customer (requires token)

**6. Inventory** (Full CRUD)
- Create, Read, Update, Delete operations
- Rate limiting and caching enabled

### Testing Features
- **Auto Token Management**: Login request saves JWT to `{{auth_token}}`
- **Sample Data**: Pre-filled request bodies
- **Documentation**: Each request includes description
- **Variables**: Use `{{baseUrl}}` for easy configuration

See `TESTING_GUIDE.md` for detailed testing instructions.

## Development Notes

### Architecture
- **Application Factory Pattern**: Enables testing and multiple configurations
- **Blueprint Organization**: Self-contained modules with routes and schemas
- **SQLAlchemy ORM**: Database abstraction and relationship management
- **Marshmallow**: Data serialization, deserialization, and validation

### Security Implementations
- **Password Hashing**: bcrypt with automatic salt generation
- **JWT Tokens**: 24-hour expiration, HS256 signing
- **Token Validation**: Middleware decorator for protected routes
- **Authorization**: Customer-specific access control

### Performance Optimizations
- **Query Optimization**: Lazy loading for relationships
- **Caching Strategy**: 5-minute TTL with automatic invalidation
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Connection Pooling**: SQLAlchemy handles database connections

### Testing
- **Postman Collection**: 40+ pre-configured requests
- **Automated Tests**: `test_api.py` for full API validation
- **Interactive Client**: `client.py` for manual testing
- **Comprehensive Guide**: `TESTING_GUIDE.md` with detailed instructions

## License
This project is for educational purposes.
