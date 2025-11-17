# Testing and Submission Guide

## ✅ Project Status: Ready for Submission

All features have been implemented and tested successfully!

## 📋 Completed Features

### Core Requirements
- ✅ **Flask-Limiter**: Rate limiting on customer and inventory creation routes (10/min for customers, 20/min for inventory)
- ✅ **Flask-Caching**: Caching implemented on GET routes for customers, mechanics, and inventory (5-minute timeout)
- ✅ **Token Authentication** (python-jose):
  - `encode_token()` function creates JWT tokens for customers
  - `login_schema` for email/password validation
  - `POST /customers/login` route returns JWT token
  - `@token_required` decorator validates tokens and extracts customer_id
  - `GET /customers/my-tickets` requires Bearer token
  - Token authentication on UPDATE and DELETE customer routes
- ✅ **Inventory Model**: Full implementation with many-to-many relationship to ServiceTicket
- ✅ **Inventory Blueprint**: Complete CRUD operations for inventory management
- ✅ **Add Part to Ticket**: Route to add inventory parts to service tickets

## 🧪 Testing in Postman

### Step 1: Import the Postman Collection
1. Open Postman
2. Click "Import" button (top left)
3. Select "Mechanic API.postman_collection.json" from your project folder
4. The collection will be imported with all endpoints organized into folders:
   - API Root
   - Customers
   - Mechanics
   - Service Tickets
   - Authentication
   - Inventory

### Step 2: Test Each Endpoint Group

#### **Authentication Flow (Recommended First)**
1. **Create a Customer** → `POST /customers/`
   - Use the sample data provided
   - Note: Password is included and will be hashed
   
2. **Customer Login** → `POST /customers/login`
   - Uses email and password from step 1
   - Returns JWT token
   - Token is **automatically saved** to environment variable `auth_token`

3. **Get My Tickets** → `GET /customers/my-tickets`
   - Requires Bearer token (automatically uses `{{auth_token}}`)
   - Returns tickets for authenticated customer

4. **Update Customer** → `PUT /customers/{id}`
   - Requires Bearer token
   - Can only update own account

5. **Delete Customer** → `DELETE /customers/{id}`
   - Requires Bearer token
   - Can only delete own account

#### **Inventory Management**
1. **Create Inventory Part** → `POST /inventory/`
   - Test rate limiting by sending 20+ requests quickly
   
2. **Get All Inventory** → `GET /inventory/`
   - First call reads from database
   - Second call within 5 minutes returns cached data (faster)

3. **Get/Update/Delete** individual parts
   - Test full CRUD functionality

#### **Service Tickets & Integration**
1. **Create Service Ticket** → `POST /service-tickets/`
   - Requires valid customer_id

2. **Assign Mechanic** → `PUT /service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}`
   - Tests many-to-many relationship

3. **Add Part to Ticket** → `PUT /service-tickets/{ticket_id}/add-part/{inventory_id}`
   - Tests inventory many-to-many relationship

### Step 3: Verify Key Features

#### Rate Limiting Test
- Send 11 requests to `POST /customers/` quickly
- The 11th request should return `429 Too Many Requests`

#### Caching Test
- Call `GET /customers/` twice
- Second request should be faster (check response time in Postman)
- Data is cached for 5 minutes

#### Token Authentication Test
- Try accessing `GET /customers/my-tickets` WITHOUT Authorization header → 401 Unauthorized
- Login and try WITH token → 200 OK with ticket data

## 📤 GitHub Submission

### Current Status
All changes are ready to commit. The following files have been modified/created:

**Modified Files:**
- `application/__init__.py` - Added inventory blueprint registration
- `application/models.py` - Added Inventory model and junction table
- `application/blueprints/service_ticket/routes.py` - Added add-part route
- `Mechanic API.postman_collection.json` - Updated with all new endpoints

**New Files:**
- `application/blueprints/inventory/__init__.py`
- `application/blueprints/inventory/routes.py`
- `application/blueprints/inventory/schemas.py`
- `test_api.py` - Automated testing script

### Commit and Push Commands

```powershell
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Add advanced features: rate limiting, caching, JWT authentication, and inventory management

- Implemented Flask-Limiter for rate limiting on customer and inventory routes
- Added Flask-Caching for GET endpoints (5-minute cache)
- Created JWT token authentication with login route and protected endpoints
- Built Inventory model with many-to-many relationship to ServiceTicket
- Developed complete Inventory blueprint with CRUD operations
- Added route to assign inventory parts to service tickets
- Updated Postman collection with all new endpoints including authentication tests"

# Push to GitHub
git push origin main
```

## 📝 Postman Collection Highlights

The exported collection includes:
- **40+ API requests** organized into 6 categories
- **Automatic token handling** (login saves token to environment)
- **Detailed descriptions** for each endpoint
- **Sample request bodies** with proper data formatting
- **Variable placeholders** for easy ID replacement

## 🎯 Testing Checklist

Before submission, verify:
- [ ] All Postman requests execute successfully
- [ ] Rate limiting triggers on excessive requests (429 response)
- [ ] Caching works (faster second request)
- [ ] Login returns JWT token
- [ ] Protected routes require Bearer token (401 without, 200 with)
- [ ] Customers can only update/delete their own accounts
- [ ] Inventory parts can be added to service tickets
- [ ] Many-to-many relationships work (mechanics and parts on tickets)

## 🚀 Running the Application

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the Flask app
python app.py
```

Application runs on: `http://127.0.0.1:5000`

---

**Project is complete and ready for submission!** ✅
