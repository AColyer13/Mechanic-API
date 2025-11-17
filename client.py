"""
Mechanic Shop API Client - Interactive Command Line Interface
This script provides a command-line interface to interact with
the Mechanic Shop API. It allows testing all endpoints with sample data
or custom input.

Run this while the Flask API is running on localhost:5000
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://127.0.0.1:5000"
HEADERS = {"Content-Type": "application/json"}

class MechanicShopAPIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.session = requests.Session()
        self.token = None
        self.logged_in_customer_id = None
        
    def make_request(self, method, endpoint, data=None, params=None, use_token=False):
        """Make HTTP request to API and handle response"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        
        # Add Authorization header if token is available and requested
        if use_token and self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                print(f"Error: Unsupported method: {method}")
                return None
                
            return self.handle_response(response)
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to API. Make sure Flask app is running on http://127.0.0.1:5000")
            return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def handle_response(self, response):
        """Handle API response and display formatted output"""
        print(f"\nStatus Code: {response.status_code}")
        
        try:
            data = response.json()
            if response.status_code in [200, 201]:
                print("✅ Success")
                print(f"Response: {json.dumps(data, indent=2, default=str)}")
            else:
                print("❌ Error Response:")
                print(f"Details: {json.dumps(data, indent=2)}")
            return data
        except json.JSONDecodeError:
            print(f"Response: {response.text}")
            return response.text

    # AUTHENTICATION
    
    def login(self):
        """POST /customers/login - Login and get JWT token"""
        print("\n🔐 Customer Login")
        print("-" * 40)
        
        email = input("Enter email: ").strip()
        if not email:
            print("❌ Email required")
            return None
        
        password = input("Enter password: ").strip()
        if not password:
            print("❌ Password required")
            return None
        
        data = {
            "email": email,
            "password": password
        }
        
        response = self.make_request('POST', '/customers/login', data)
        if response and 'token' in response:
            self.token = response['token']
            self.logged_in_customer_id = response.get('customer_id')
            print(f"\n✅ Login successful!")
            print(f"👤 Logged in as Customer ID: {self.logged_in_customer_id}")
            print(f"🔑 Token: {self.token[:20]}...")
        return response
    
    def logout(self):
        """Logout and clear token"""
        if self.token:
            print("\n👋 Logging out...")
            self.token = None
            self.logged_in_customer_id = None
            print("✅ Logged out successfully")
        else:
            print("\nℹ️ Not currently logged in")
    
    def get_my_tickets(self):
        """GET /customers/my-tickets - Get tickets for logged-in customer (requires token)"""
        print("\n🎫 Getting My Service Tickets")
        print("-" * 40)
        
        if not self.token:
            print("❌ Please login first (option 21)")
            return None
        
        return self.make_request('GET', '/customers/my-tickets', use_token=True)
    
    # CUSTOMER ENDPOINTS
    
    def create_customer(self):
        """POST /customers - Create new customer"""
        print("\n🔧 Creating New Customer")
        print("-" * 40)
        
        while True:
            first_name = input("Enter first name (required): ").strip()
            if first_name:
                break
            print("❌ Required field!")
        
        while True:
            last_name = input("Enter last name (required): ").strip()
            if last_name:
                break
            print("❌ Required field!")
        
        while True:
            email = input("Enter email (required): ").strip()
            if email and '@' in email:
                break
            print("❌ Valid email required!")
        
        while True:
            password = input("Enter password (required): ").strip()
            if password and len(password) >= 6:
                break
            print("❌ Password must be at least 6 characters!")
        
        phone = input("Enter phone (optional): ").strip()
        address = input("Enter address (optional): ").strip()
        
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
        
        print(f"Creating customer with data: {json.dumps(data, indent=2)}")
        return self.make_request('POST', '/customers/', data)
    
    def get_all_customers(self):
        """GET /customers - Get all customers"""
        print("\n👥 Getting All Customers")
        print("-" * 40)
        return self.make_request('GET', '/customers/')
    
    def get_customer_by_id(self):
        """GET /customers/<id> - Get customer by ID"""
        print("\n🔍 Getting Customer by ID")
        print("-" * 40)
        customer_id = input("Enter Customer ID: ").strip()
        if not customer_id.isdigit():
            print("❌ Invalid Customer ID")
            return None
        return self.make_request('GET', f'/customers/{customer_id}')
    
    def update_customer(self):
        """PUT /customers/<id> - Update customer (requires token)"""
        print("\n✏️ Updating Customer")
        print("-" * 40)
        
        if not self.token:
            print("❌ Please login first (option 21)")
            return None
        
        # Default to logged-in customer's ID
        default_id = str(self.logged_in_customer_id) if self.logged_in_customer_id else ""
        customer_id = input(f"Enter Customer ID to update [{default_id}]: ").strip()
        if not customer_id and default_id:
            customer_id = default_id
        if not customer_id.isdigit():
            print("❌ Invalid Customer ID")
            return None
            
        first_name = input("Enter new first name (leave blank to keep current): ").strip()
        last_name = input("Enter new last name (leave blank to keep current): ").strip()
        email = input("Enter new email (leave blank to keep current): ").strip()
        phone = input("Enter new phone (leave blank to keep current): ").strip()
        address = input("Enter new address (leave blank to keep current): ").strip()
        
        data = {}
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
            
        if not data:
            print("❌ No changes specified")
            return None
            
        return self.make_request('PUT', f'/customers/{customer_id}', data, use_token=True)
    
    def delete_customer(self):
        """DELETE /customers/<id> - Delete customer (requires token)"""
        print("\n🗑️ Deleting Customer")
        print("-" * 40)
        
        if not self.token:
            print("❌ Please login first (option 21)")
            return None
        
        # Default to logged-in customer's ID
        default_id = str(self.logged_in_customer_id) if self.logged_in_customer_id else ""
        customer_id = input(f"Enter Customer ID to delete [{default_id}]: ").strip()
        if not customer_id and default_id:
            customer_id = default_id
        if not customer_id.isdigit():
            print("❌ Invalid Customer ID")
            return None
            
        confirm = input(f"⚠️ Are you sure you want to delete customer {customer_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            result = self.make_request('DELETE', f'/customers/{customer_id}', use_token=True)
            if result and 'message' in result:
                self.logout()  # Auto-logout after deleting own account
            return result
        else:
            print("🚫 Deletion cancelled")
            return None

    # MECHANIC ENDPOINTS
    
    def create_mechanic(self):
        """POST /mechanics - Create new mechanic"""
        print("\n🔧 Creating New Mechanic")
        print("-" * 40)
        
        while True:
            first_name = input("Enter first name (required): ").strip()
            if first_name:
                break
            print("❌ Required field!")
        
        while True:
            last_name = input("Enter last name (required): ").strip()
            if last_name:
                break
            print("❌ Required field!")
        
        while True:
            email = input("Enter email (required): ").strip()
            if email and '@' in email:
                break
            print("❌ Valid email required!")
        
        phone = input("Enter phone (optional): ").strip()
        specialty = input("Enter specialty (optional): ").strip()
        
        hourly_rate_input = input("Enter hourly rate (optional): ").strip()
        hourly_rate = None
        if hourly_rate_input:
            try:
                hourly_rate = float(hourly_rate_input)
            except ValueError:
                print("⚠️ Invalid hourly rate, skipping")
        
        hire_date_input = input("Enter hire date (YYYY-MM-DD, optional): ").strip()
        hire_date = None
        if hire_date_input:
            try:
                datetime.strptime(hire_date_input, '%Y-%m-%d')
                hire_date = hire_date_input
            except ValueError:
                print("⚠️ Invalid date format, skipping")
        
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
        
        if phone:
            data["phone"] = phone
        if specialty:
            data["specialty"] = specialty
        if hourly_rate:
            data["hourly_rate"] = hourly_rate
        if hire_date:
            data["hire_date"] = hire_date
        
        print(f"Creating mechanic with data: {json.dumps(data, indent=2)}")
        return self.make_request('POST', '/mechanics/', data)
    
    def get_all_mechanics(self):
        """GET /mechanics - Get all mechanics"""
        print("\n🔧 Getting All Mechanics")
        print("-" * 40)
        return self.make_request('GET', '/mechanics/')
    
    def get_mechanic_by_id(self):
        """GET /mechanics/<id> - Get mechanic by ID"""
        print("\n🔍 Getting Mechanic by ID")
        print("-" * 40)
        mechanic_id = input("Enter Mechanic ID: ").strip()
        if not mechanic_id.isdigit():
            print("❌ Invalid Mechanic ID")
            return None
        return self.make_request('GET', f'/mechanics/{mechanic_id}')
    
    def update_mechanic(self):
        """PUT /mechanics/<id> - Update mechanic"""
        print("\n✏️ Updating Mechanic")
        print("-" * 40)
        mechanic_id = input("Enter Mechanic ID to update: ").strip()
        if not mechanic_id.isdigit():
            print("❌ Invalid Mechanic ID")
            return None
            
        first_name = input("Enter new first name (leave blank to keep current): ").strip()
        last_name = input("Enter new last name (leave blank to keep current): ").strip()
        email = input("Enter new email (leave blank to keep current): ").strip()
        phone = input("Enter new phone (leave blank to keep current): ").strip()
        specialty = input("Enter new specialty (leave blank to keep current): ").strip()
        hourly_rate = input("Enter new hourly rate (leave blank to keep current): ").strip()
        
        data = {}
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if specialty:
            data["specialty"] = specialty
        if hourly_rate:
            try:
                data["hourly_rate"] = float(hourly_rate)
            except ValueError:
                print("⚠️ Invalid hourly rate, skipping")
            
        if not data:
            print("❌ No changes specified")
            return None
            
        return self.make_request('PUT', f'/mechanics/{mechanic_id}', data)
    
    def delete_mechanic(self):
        """DELETE /mechanics/<id> - Delete mechanic"""
        print("\n🗑️ Deleting Mechanic")
        print("-" * 40)
        mechanic_id = input("Enter Mechanic ID to delete: ").strip()
        if not mechanic_id.isdigit():
            print("❌ Invalid Mechanic ID")
            return None
            
        confirm = input(f"⚠️ Are you sure you want to delete mechanic {mechanic_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.make_request('DELETE', f'/mechanics/{mechanic_id}')
        else:
            print("🚫 Deletion cancelled")
            return None

    # SERVICE TICKET ENDPOINTS
    
    def create_service_ticket(self):
        """POST /service-tickets - Create new service ticket"""
        print("\n🎫 Creating New Service Ticket")
        print("-" * 40)
        
        customer_id = input("Enter Customer ID (required): ").strip()
        if not customer_id.isdigit():
            print("❌ Invalid Customer ID")
            return None
        
        while True:
            description = input("Enter description of work needed (required): ").strip()
            if description:
                break
            print("❌ Required field!")
        
        vehicle_year = input("Enter vehicle year (optional): ").strip()
        vehicle_make = input("Enter vehicle make (optional): ").strip()
        vehicle_model = input("Enter vehicle model (optional): ").strip()
        vehicle_vin = input("Enter vehicle VIN (optional): ").strip()
        
        estimated_cost_input = input("Enter estimated cost (optional): ").strip()
        estimated_cost = None
        if estimated_cost_input:
            try:
                estimated_cost = float(estimated_cost_input)
            except ValueError:
                print("⚠️ Invalid cost, skipping")
        
        print("Available statuses: Open, In Progress, Completed, Cancelled")
        status = input("Enter status (default: Open): ").strip()
        if not status:
            status = "Open"
        
        data = {
            "customer_id": int(customer_id),
            "description": description
        }
        
        if vehicle_year and vehicle_year.isdigit():
            data["vehicle_year"] = int(vehicle_year)
        if vehicle_make:
            data["vehicle_make"] = vehicle_make
        if vehicle_model:
            data["vehicle_model"] = vehicle_model
        if vehicle_vin:
            data["vehicle_vin"] = vehicle_vin
        if estimated_cost:
            data["estimated_cost"] = estimated_cost
        if status:
            data["status"] = status
        
        print(f"Creating service ticket with data: {json.dumps(data, indent=2)}")
        return self.make_request('POST', '/service-tickets/', data)
    
    def get_all_service_tickets(self):
        """GET /service-tickets - Get all service tickets"""
        print("\n🎫 Getting All Service Tickets")
        print("-" * 40)
        return self.make_request('GET', '/service-tickets/')
    
    def get_service_ticket_by_id(self):
        """GET /service-tickets/<id> - Get service ticket by ID"""
        print("\n🔍 Getting Service Ticket by ID")
        print("-" * 40)
        ticket_id = input("Enter Service Ticket ID: ").strip()
        if not ticket_id.isdigit():
            print("❌ Invalid Service Ticket ID")
            return None
        return self.make_request('GET', f'/service-tickets/{ticket_id}')
    
    def update_service_ticket(self):
        """PUT /service-tickets/<id> - Update service ticket"""
        print("\n✏️ Updating Service Ticket")
        print("-" * 40)
        ticket_id = input("Enter Service Ticket ID to update: ").strip()
        if not ticket_id.isdigit():
            print("❌ Invalid Service Ticket ID")
            return None
            
        description = input("Enter new description (leave blank to keep current): ").strip()
        actual_cost = input("Enter actual cost (leave blank to keep current): ").strip()
        print("Available statuses: Open, In Progress, Completed, Cancelled")
        status = input("Enter new status (leave blank to keep current): ").strip()
        
        data = {}
        if description:
            data["description"] = description
        if actual_cost:
            try:
                data["actual_cost"] = float(actual_cost)
            except ValueError:
                print("⚠️ Invalid cost, skipping")
        if status:
            data["status"] = status
            
        if not data:
            print("❌ No changes specified")
            return None
            
        return self.make_request('PUT', f'/service-tickets/{ticket_id}', data)
    
    def delete_service_ticket(self):
        """DELETE /service-tickets/<id> - Delete service ticket"""
        print("\n🗑️ Deleting Service Ticket")
        print("-" * 40)
        ticket_id = input("Enter Service Ticket ID to delete: ").strip()
        if not ticket_id.isdigit():
            print("❌ Invalid Service Ticket ID")
            return None
            
        confirm = input(f"⚠️ Are you sure you want to delete service ticket {ticket_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            return self.make_request('DELETE', f'/service-tickets/{ticket_id}')
        else:
            print("🚫 Deletion cancelled")
            return None
    
    def assign_mechanic_to_ticket(self):
        """PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> - Assign mechanic"""
        print("\n🔧 Assigning Mechanic to Service Ticket")
        print("-" * 40)
        ticket_id = input("Enter Service Ticket ID: ").strip()
        mechanic_id = input("Enter Mechanic ID to assign: ").strip()
        
        if not ticket_id.isdigit() or not mechanic_id.isdigit():
            print("❌ Invalid Service Ticket ID or Mechanic ID")
            return None
            
        return self.make_request('PUT', f'/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}')
    
    def remove_mechanic_from_ticket(self):
        """PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id> - Remove mechanic"""
        print("\n🚫 Removing Mechanic from Service Ticket")
        print("-" * 40)
        ticket_id = input("Enter Service Ticket ID: ").strip()
        mechanic_id = input("Enter Mechanic ID to remove: ").strip()
        
        if not ticket_id.isdigit() or not mechanic_id.isdigit():
            print("❌ Invalid Service Ticket ID or Mechanic ID")
            return None
            
        return self.make_request('PUT', f'/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}')
    
    def get_tickets_by_customer(self):
        """GET /service-tickets/customer/<customer_id> - Get tickets by customer"""
        print("\n👤 Getting Tickets by Customer")
        print("-" * 40)
        customer_id = input("Enter Customer ID: ").strip()
        if not customer_id.isdigit():
            print("❌ Invalid Customer ID")
            return None
        return self.make_request('GET', f'/service-tickets/customer/{customer_id}')
    
    def get_tickets_by_mechanic(self):
        """GET /service-tickets/mechanic/<mechanic_id> - Get tickets by mechanic"""
        print("\n🔧 Getting Tickets by Mechanic")
        print("-" * 40)
        mechanic_id = input("Enter Mechanic ID: ").strip()
        if not mechanic_id.isdigit():
            print("❌ Invalid Mechanic ID")
            return None
        return self.make_request('GET', f'/service-tickets/mechanic/{mechanic_id}')

    # AUTOMATED TESTING
    
    def run_complete_test_suite(self):
        """Run a complete test of all endpoints with sample data"""
        print("\n🧪 Running Complete Test Suite")
        print("=" * 60)
        
        print("\n1. Creating sample customers...")
        customer_ids = []
        sample_customers = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john.doe.{datetime.now().strftime('%H%M%S')}@email.com",
                "phone": "555-0001",
                "address": "123 Main St, City, State"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": f"jane.smith.{datetime.now().strftime('%H%M%S')}@email.com",
                "phone": "555-0002",
                "address": "456 Oak Ave, City, State"
            }
        ]
        
        for customer_data in sample_customers:
            print(f"  Creating customer: {customer_data['first_name']} {customer_data['last_name']}")
            response = self.make_request('POST', '/customers/', customer_data)
            if response and 'id' in response:
                customer_ids.append(response['id'])
        
        print("\n2. Creating sample mechanics...")
        mechanic_ids = []
        sample_mechanics = [
            {
                "first_name": "Mike",
                "last_name": "Johnson",
                "email": f"mike.johnson.{datetime.now().strftime('%H%M%S')}@mechanicshop.com",
                "phone": "555-1001",
                "specialty": "Engine Repair",
                "hourly_rate": 85.00,
                "hire_date": "2023-01-15"
            },
            {
                "first_name": "Sarah",
                "last_name": "Williams",
                "email": f"sarah.williams.{datetime.now().strftime('%H%M%S')}@mechanicshop.com",
                "phone": "555-1002",
                "specialty": "Transmission",
                "hourly_rate": 90.00,
                "hire_date": "2023-03-01"
            }
        ]
        
        for mechanic_data in sample_mechanics:
            print(f"  Creating mechanic: {mechanic_data['first_name']} {mechanic_data['last_name']}")
            response = self.make_request('POST', '/mechanics/', mechanic_data)
            if response and 'id' in response:
                mechanic_ids.append(response['id'])
        
        print("\n3. Getting all customers...")
        self.get_all_customers()
        
        print("\n4. Getting all mechanics...")
        self.get_all_mechanics()
        
        print("\n5. Creating service tickets...")
        ticket_ids = []
        sample_tickets = [
            {
                "customer_id": customer_ids[0] if customer_ids else 1,
                "vehicle_year": 2020,
                "vehicle_make": "Toyota",
                "vehicle_model": "Camry",
                "vehicle_vin": "1234567890ABCDEFG",
                "description": "Engine making strange noise",
                "estimated_cost": 500.00,
                "status": "Open"
            },
            {
                "customer_id": customer_ids[1] if len(customer_ids) > 1 else 1,
                "vehicle_year": 2019,
                "vehicle_make": "Honda",
                "vehicle_model": "Accord",
                "description": "Brake pads need replacement",
                "estimated_cost": 300.00,
                "status": "Open"
            }
        ]
        
        for ticket_data in sample_tickets:
            print(f"  Creating ticket for customer {ticket_data['customer_id']}")
            response = self.make_request('POST', '/service-tickets/', ticket_data)
            if response and 'id' in response:
                ticket_ids.append(response['id'])
        
        print("\n6. Assigning mechanics to tickets...")
        if ticket_ids and mechanic_ids:
            for i, ticket_id in enumerate(ticket_ids):
                mechanic_id = mechanic_ids[i % len(mechanic_ids)]
                print(f"  Assigning mechanic {mechanic_id} to ticket {ticket_id}")
                self.make_request('PUT', f'/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}')
        
        print("\n7. Getting service tickets...")
        self.get_all_service_tickets()
        
        print("\n8. Updating ticket status...")
        if ticket_ids:
            data = {"status": "In Progress"}
            print(f"  Updating ticket {ticket_ids[0]} to In Progress")
            self.make_request('PUT', f'/service-tickets/{ticket_ids[0]}', data)
        
        print("\n9. Getting tickets by customer...")
        if customer_ids:
            self.make_request('GET', f'/service-tickets/customer/{customer_ids[0]}')
        
        print("\n10. Getting tickets by mechanic...")
        if mechanic_ids:
            self.make_request('GET', f'/service-tickets/mechanic/{mechanic_ids[0]}')
        
        print("\n✅ Complete test suite finished!")
        print(f"Created {len(customer_ids)} customers, {len(mechanic_ids)} mechanics, {len(ticket_ids)} service tickets")


def display_main_menu(client):
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("🔧 MECHANIC SHOP API CLIENT 🔧")
    print("=" * 60)
    
    # Show login status
    if client.token:
        print(f"🔐 Logged in as Customer ID: {client.logged_in_customer_id}")
    else:
        print("🔓 Not logged in")
    print("=" * 60)
    
    print("AUTHENTICATION:")
    print("  21. Login (Get JWT Token)")
    print("  22. Logout")
    print("  23. Get My Tickets (requires login)")
    print("\nCUSTOMER OPERATIONS:")
    print("  1.  Create Customer (with password)")
    print("  2.  Get All Customers") 
    print("  3.  Get Customer by ID")
    print("  4.  Update Customer (requires login)")
    print("  5.  Delete Customer (requires login)")
    print("\nMECHANIC OPERATIONS:")
    print("  6.  Create Mechanic")
    print("  7.  Get All Mechanics")
    print("  8.  Get Mechanic by ID") 
    print("  9.  Update Mechanic")
    print("  10. Delete Mechanic")
    print("\nSERVICE TICKET OPERATIONS:")
    print("  11. Create Service Ticket")
    print("  12. Get All Service Tickets")
    print("  13. Get Service Ticket by ID")
    print("  14. Update Service Ticket")
    print("  15. Delete Service Ticket")
    print("  16. Assign Mechanic to Ticket")
    print("  17. Remove Mechanic from Ticket")
    print("  18. Get Tickets by Customer")
    print("  19. Get Tickets by Mechanic")
    print("\nAUTOMATED TESTING:")
    print("  20. Run Complete Test Suite")
    print("\n  0.  Exit")
    print("-" * 60)


def main():
    """Main application loop"""
    client = MechanicShopAPIClient()
    
    print("🔧 Starting Mechanic Shop API Client...")
    print("🔍 Checking for Flask API...")
    
    # Try multiple possible URLs where Flask might be running
    possible_urls = [
        "http://127.0.0.1:5000",
        "http://localhost:5000", 
        "http://0.0.0.0:5000",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ]
    
    connected = False
    working_url = None
    
    for url in possible_urls:
        try:
            print(f"🔄 Trying {url}...")
            response = requests.get(f"{url}/", timeout=5)
            if response.status_code == 200:
                print(f"✅ Connected to API successfully at {url}!")
                try:
                    data = response.json()
                    print(f"📋 API Message: {data.get('message', 'N/A')}")
                    print(f"🔗 Available endpoints: {data.get('endpoints', {})}")
                except json.JSONDecodeError:
                    print("⚠️ API responded but didn't return JSON")
                connected = True
                working_url = url
                # Update the client's base URL
                client.base_url = url
                break
            else:
                print(f"❌ Got response code {response.status_code} from {url}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection refused at {url}")
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout connecting to {url}")
        except Exception as e:
            print(f"❌ Error with {url}: {str(e)[:50]}...")
    
    if not connected:
        print("\n" + "="*70)
        print("❌ FLASK API NOT RUNNING")
        print("="*70)
        print("📝 To start your Flask API:")
        print("   1. Open a new terminal/command prompt")
        print("   2. Navigate to your project directory:")
        print("      cd \"c:\\Users\\adamc\\OneDrive\\Coding Temple\\Mechanic API\"")
        print("   3. Start the Flask app:")
        print("      .venv\\Scripts\\python.exe app.py")
        print("   4. Wait for message: '* Running on http://127.0.0.1:5000'")
        print("   5. Then run this client again")
        print("\n🔧 If you get database errors when starting Flask:")
        print("   • Make sure MySQL is running (I can see it is from your image)")
        print("   • Create the database if it doesn't exist:")
        print("     mysql -u root -p")
        print("     CREATE DATABASE mechanicshopdata;")
        print("     exit;")
        print("\n⚠️ Common issues:")
        print("   • Port 5000 might be in use - Flask will show alternative port")
        print("   • Virtual environment might not be activated")
        print("   • Missing dependencies - run: .venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        print("="*70)
        
        choice = input("\n🤔 Continue with client anyway? (y/N): ").strip().lower()
        if choice != 'y':
            print("👋 Exiting... Start Flask API first, then run client again.")
            return
    else:
        print(f"\n🎉 Ready to use API at: {working_url}")

    while True:
        display_main_menu(client)
        choice = input("Enter your choice (0-23): ").strip()
        
        try:
            if choice == '0':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                client.create_customer()
            elif choice == '2':
                client.get_all_customers()
            elif choice == '3':
                client.get_customer_by_id()
            elif choice == '4':
                client.update_customer()
            elif choice == '5':
                client.delete_customer()
            elif choice == '6':
                client.create_mechanic()
            elif choice == '7':
                client.get_all_mechanics()
            elif choice == '8':
                client.get_mechanic_by_id()
            elif choice == '9':
                client.update_mechanic()
            elif choice == '10':
                client.delete_mechanic()
            elif choice == '11':
                client.create_service_ticket()
            elif choice == '12':
                client.get_all_service_tickets()
            elif choice == '13':
                client.get_service_ticket_by_id()
            elif choice == '14':
                client.update_service_ticket()
            elif choice == '15':
                client.delete_service_ticket()
            elif choice == '16':
                client.assign_mechanic_to_ticket()
            elif choice == '17':
                client.remove_mechanic_from_ticket()
            elif choice == '18':
                client.get_tickets_by_customer()
            elif choice == '19':
                client.get_tickets_by_mechanic()
            elif choice == '20':
                confirm = input("🧪 This will create sample data. Continue? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.run_complete_test_suite()
                else:
                    print("🚫 Test suite cancelled")
            elif choice == '21':
                client.login()
            elif choice == '22':
                client.logout()
            elif choice == '23':
                client.get_my_tickets()
            else:
                print("❌ Invalid choice. Please select 0-23.")
                
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
