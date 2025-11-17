#!/usr/bin/env python3
"""
Mechanic Shop API Client

A comprehensive Python client for interacting with the Mechanic Shop API.
Supports all CRUD operations for customers, mechanics, inventory, and service tickets.
Includes authentication, error handling, and a user-friendly CLI interface.

Usage:
    python api_client.py
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys


class MechanicAPIClient:
    """Client for interacting with the Mechanic Shop API."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        """Initialize the API client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.authenticated_customer_id = None
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            print(f"❌ Error: Could not connect to API server at {self.base_url}")
            print("Make sure the Flask application is running!")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            sys.exit(1)
    
    def set_auth_token(self, token: str):
        """Set authentication token for protected endpoints.
        
        Args:
            token: JWT token
        """
        self.token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def clear_auth_token(self):
        """Clear authentication token."""
        self.token = None
        self.authenticated_customer_id = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    # =============================================================================
    # CUSTOMER OPERATIONS
    # =============================================================================
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer.
        
        Args:
            customer_data: Customer information including password
            
        Returns:
            Created customer data
        """
        response = self._make_request('POST', '/customers/', json=customer_data)
        if response.status_code == 201:
            print("✅ Customer created successfully!")
            return response.json()
        else:
            print(f"❌ Failed to create customer: {response.status_code}")
            print(response.json())
            return {}
    
    def login_customer(self, email: str, password: str) -> bool:
        """Login customer and store authentication token.
        
        Args:
            email: Customer email
            password: Customer password
            
        Returns:
            True if login successful, False otherwise
        """
        login_data = {"email": email, "password": password}
        response = self._make_request('POST', '/customers/login', json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.set_auth_token(data['token'])
            self.authenticated_customer_id = data.get('customer_id')
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed: {response.json().get('message', 'Unknown error')}")
            return False
    
    def get_customers(self, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get all customers with pagination.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            List of customers
        """
        params = {'page': page, 'per_page': per_page}
        response = self._make_request('GET', '/customers/', params=params)
        
        if response.status_code == 200:
            data = response.json()
            customers = data.get('customers', [])
            print(f"📋 Retrieved {len(customers)} customers (Page {page})")
            return customers
        else:
            print(f"❌ Failed to get customers: {response.status_code}")
            return []
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Get a specific customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Customer data
        """
        response = self._make_request('GET', f'/customers/{customer_id}')
        
        if response.status_code == 200:
            print(f"👤 Retrieved customer {customer_id}")
            return response.json()
        else:
            print(f"❌ Failed to get customer: {response.status_code}")
            return {}
    
    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a customer.
        
        Args:
            customer_id: Customer ID
            customer_data: Updated customer information
            
        Returns:
            Updated customer data
        """
        response = self._make_request('PUT', f'/customers/{customer_id}', json=customer_data)
        
        if response.status_code == 200:
            print(f"✅ Customer {customer_id} updated successfully!")
            return response.json()
        else:
            print(f"❌ Failed to update customer: {response.status_code}")
            print(response.json())
            return {}
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('DELETE', f'/customers/{customer_id}')
        
        if response.status_code == 200:
            print(f"✅ Customer {customer_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete customer: {response.status_code}")
            return False
    
    # =============================================================================
    # MECHANIC OPERATIONS
    # =============================================================================
    
    def create_mechanic(self, mechanic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new mechanic.
        
        Args:
            mechanic_data: Mechanic information
            
        Returns:
            Created mechanic data
        """
        response = self._make_request('POST', '/mechanics/', json=mechanic_data)
        
        if response.status_code == 201:
            print("✅ Mechanic created successfully!")
            return response.json()
        else:
            print(f"❌ Failed to create mechanic: {response.status_code}")
            print(response.json())
            return {}
    
    def get_mechanics(self) -> List[Dict[str, Any]]:
        """Get all mechanics.
        
        Returns:
            List of mechanics
        """
        response = self._make_request('GET', '/mechanics/')
        
        if response.status_code == 200:
            mechanics = response.json()
            print(f"🔧 Retrieved {len(mechanics)} mechanics")
            return mechanics
        else:
            print(f"❌ Failed to get mechanics: {response.status_code}")
            return []
    
    def get_mechanics_by_workload(self) -> List[Dict[str, Any]]:
        """Get mechanics ordered by workload (ticket count).
        
        Returns:
            List of mechanics with ticket counts
        """
        response = self._make_request('GET', '/mechanics/by-workload')
        
        if response.status_code == 200:
            mechanics = response.json()
            print(f"📊 Retrieved {len(mechanics)} mechanics by workload")
            return mechanics
        else:
            print(f"❌ Failed to get mechanics by workload: {response.status_code}")
            return []
    
    def get_mechanic(self, mechanic_id: int) -> Dict[str, Any]:
        """Get a specific mechanic by ID.
        
        Args:
            mechanic_id: Mechanic ID
            
        Returns:
            Mechanic data
        """
        response = self._make_request('GET', f'/mechanics/{mechanic_id}')
        
        if response.status_code == 200:
            print(f"🔧 Retrieved mechanic {mechanic_id}")
            return response.json()
        else:
            print(f"❌ Failed to get mechanic: {response.status_code}")
            return {}
    
    def update_mechanic(self, mechanic_id: int, mechanic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a mechanic.
        
        Args:
            mechanic_id: Mechanic ID
            mechanic_data: Updated mechanic information
            
        Returns:
            Updated mechanic data
        """
        response = self._make_request('PUT', f'/mechanics/{mechanic_id}', json=mechanic_data)
        
        if response.status_code == 200:
            print(f"✅ Mechanic {mechanic_id} updated successfully!")
            return response.json()
        else:
            print(f"❌ Failed to update mechanic: {response.status_code}")
            print(response.json())
            return {}
    
    def delete_mechanic(self, mechanic_id: int) -> bool:
        """Delete a mechanic.
        
        Args:
            mechanic_id: Mechanic ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('DELETE', f'/mechanics/{mechanic_id}')
        
        if response.status_code == 200:
            print(f"✅ Mechanic {mechanic_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete mechanic: {response.status_code}")
            return False
    
    # =============================================================================
    # INVENTORY OPERATIONS
    # =============================================================================
    
    def create_inventory_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new inventory item (requires authentication).
        
        Args:
            item_data: Inventory item information
            
        Returns:
            Created inventory item data
        """
        response = self._make_request('POST', '/inventory/', json=item_data)
        
        if response.status_code == 201:
            print("✅ Inventory item created successfully!")
            return response.json()
        else:
            print(f"❌ Failed to create inventory item: {response.status_code}")
            print(response.json())
            return {}
    
    def get_inventory(self) -> List[Dict[str, Any]]:
        """Get all inventory items.
        
        Returns:
            List of inventory items
        """
        response = self._make_request('GET', '/inventory/')
        
        if response.status_code == 200:
            inventory = response.json()
            print(f"📦 Retrieved {len(inventory)} inventory items")
            return inventory
        else:
            print(f"❌ Failed to get inventory: {response.status_code}")
            return []
    
    def get_inventory_item(self, item_id: int) -> Dict[str, Any]:
        """Get a specific inventory item by ID.
        
        Args:
            item_id: Inventory item ID
            
        Returns:
            Inventory item data
        """
        response = self._make_request('GET', f'/inventory/{item_id}')
        
        if response.status_code == 200:
            print(f"📦 Retrieved inventory item {item_id}")
            return response.json()
        else:
            print(f"❌ Failed to get inventory item: {response.status_code}")
            return {}
    
    def update_inventory_item(self, item_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an inventory item (requires authentication).
        
        Args:
            item_id: Inventory item ID
            item_data: Updated inventory item information
            
        Returns:
            Updated inventory item data
        """
        response = self._make_request('PUT', f'/inventory/{item_id}', json=item_data)
        
        if response.status_code == 200:
            print(f"✅ Inventory item {item_id} updated successfully!")
            return response.json()
        else:
            print(f"❌ Failed to update inventory item: {response.status_code}")
            print(response.json())
            return {}
    
    def delete_inventory_item(self, item_id: int) -> bool:
        """Delete an inventory item (requires authentication).
        
        Args:
            item_id: Inventory item ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('DELETE', f'/inventory/{item_id}')
        
        if response.status_code == 200:
            print(f"✅ Inventory item {item_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete inventory item: {response.status_code}")
            return False
    
    # =============================================================================
    # SERVICE TICKET OPERATIONS
    # =============================================================================
    
    def create_service_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new service ticket.
        
        Args:
            ticket_data: Service ticket information
            
        Returns:
            Created service ticket data
        """
        response = self._make_request('POST', '/service-tickets/', json=ticket_data)
        
        if response.status_code == 201:
            print("✅ Service ticket created successfully!")
            return response.json()
        else:
            print(f"❌ Failed to create service ticket: {response.status_code}")
            print(response.json())
            return {}
    
    def get_service_tickets(self) -> List[Dict[str, Any]]:
        """Get all service tickets.
        
        Returns:
            List of service tickets
        """
        response = self._make_request('GET', '/service-tickets/')
        
        if response.status_code == 200:
            tickets = response.json()
            print(f"🎫 Retrieved {len(tickets)} service tickets")
            return tickets
        else:
            print(f"❌ Failed to get service tickets: {response.status_code}")
            return []
    
    def get_service_ticket(self, ticket_id: int) -> Dict[str, Any]:
        """Get a specific service ticket by ID.
        
        Args:
            ticket_id: Service ticket ID
            
        Returns:
            Service ticket data
        """
        response = self._make_request('GET', f'/service-tickets/{ticket_id}')
        
        if response.status_code == 200:
            print(f"🎫 Retrieved service ticket {ticket_id}")
            return response.json()
        else:
            print(f"❌ Failed to get service ticket: {response.status_code}")
            return {}
    
    def update_service_ticket(self, ticket_id: int, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a service ticket.
        
        Args:
            ticket_id: Service ticket ID
            ticket_data: Updated service ticket information
            
        Returns:
            Updated service ticket data
        """
        response = self._make_request('PUT', f'/service-tickets/{ticket_id}', json=ticket_data)
        
        if response.status_code == 200:
            print(f"✅ Service ticket {ticket_id} updated successfully!")
            return response.json()
        else:
            print(f"❌ Failed to update service ticket: {response.status_code}")
            print(response.json())
            return {}
    
    def delete_service_ticket(self, ticket_id: int) -> bool:
        """Delete a service ticket.
        
        Args:
            ticket_id: Service ticket ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('DELETE', f'/service-tickets/{ticket_id}')
        
        if response.status_code == 200:
            print(f"✅ Service ticket {ticket_id} deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete service ticket: {response.status_code}")
            return False
    
    def assign_mechanic_to_ticket(self, ticket_id: int, mechanic_id: int) -> bool:
        """Assign a mechanic to a service ticket.
        
        Args:
            ticket_id: Service ticket ID
            mechanic_id: Mechanic ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('PUT', f'/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}')
        
        if response.status_code == 200:
            print(f"✅ Mechanic {mechanic_id} assigned to ticket {ticket_id}!")
            return True
        else:
            print(f"❌ Failed to assign mechanic: {response.status_code}")
            return False
    
    def remove_mechanic_from_ticket(self, ticket_id: int, mechanic_id: int) -> bool:
        """Remove a mechanic from a service ticket.
        
        Args:
            ticket_id: Service ticket ID
            mechanic_id: Mechanic ID
            
        Returns:
            True if successful, False otherwise
        """
        response = self._make_request('PUT', f'/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}')
        
        if response.status_code == 200:
            print(f"✅ Mechanic {mechanic_id} removed from ticket {ticket_id}!")
            return True
        else:
            print(f"❌ Failed to remove mechanic: {response.status_code}")
            return False
    
    def bulk_edit_ticket_mechanics(self, ticket_id: int, add_ids: List[int] = None, remove_ids: List[int] = None) -> bool:
        """Bulk add/remove mechanics from a service ticket.
        
        Args:
            ticket_id: Service ticket ID
            add_ids: List of mechanic IDs to add
            remove_ids: List of mechanic IDs to remove
            
        Returns:
            True if successful, False otherwise
        """
        data = {}
        if add_ids:
            data['add_ids'] = add_ids
        if remove_ids:
            data['remove_ids'] = remove_ids
        
        response = self._make_request('PUT', f'/service-tickets/{ticket_id}/edit', json=data)
        
        if response.status_code == 200:
            print(f"✅ Mechanics updated for ticket {ticket_id}!")
            return True
        else:
            print(f"❌ Failed to update mechanics: {response.status_code}")
            return False
    
    def get_customer_tickets(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all service tickets for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List of service tickets
        """
        response = self._make_request('GET', f'/service-tickets/customer/{customer_id}')
        
        if response.status_code == 200:
            tickets = response.json()
            print(f"🎫 Retrieved {len(tickets)} tickets for customer {customer_id}")
            return tickets
        else:
            print(f"❌ Failed to get customer tickets: {response.status_code}")
            return []
    
    def get_mechanic_tickets(self, mechanic_id: int) -> List[Dict[str, Any]]:
        """Get all service tickets for a mechanic.
        
        Args:
            mechanic_id: Mechanic ID
            
        Returns:
            List of service tickets
        """
        response = self._make_request('GET', f'/service-tickets/mechanic/{mechanic_id}')
        
        if response.status_code == 200:
            tickets = response.json()
            print(f"🎫 Retrieved {len(tickets)} tickets for mechanic {mechanic_id}")
            return tickets
        else:
            print(f"❌ Failed to get mechanic tickets: {response.status_code}")
            return []


# =============================================================================
# INTERACTIVE CLI INTERFACE
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("🔧 MECHANIC SHOP API CLIENT")
    print("="*60)
    print("1.  👤 Customer Operations")
    print("2.  🔧 Mechanic Operations") 
    print("3.  📦 Inventory Operations")
    print("4.  🎫 Service Ticket Operations")
    print("5.  🔐 Authentication")
    print("6.  📊 Reports & Analytics")
    print("0.  ❌ Exit")
    print("="*60)


def customer_menu(client: MechanicAPIClient):
    """Handle customer operations."""
    while True:
        print("\n👤 CUSTOMER OPERATIONS")
        print("1. Create Customer")
        print("2. List Customers") 
        print("3. Get Customer by ID")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n📝 CREATE CUSTOMER")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            phone = input("Phone (optional): ").strip()
            address = input("Address (optional): ").strip()
            
            customer_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            }
            if phone:
                customer_data["phone"] = phone
            if address:
                customer_data["address"] = address
            
            result = client.create_customer(customer_data)
            if result:
                print(f"Customer ID: {result.get('id')}")
        
        elif choice == '2':
            print("\n📋 LIST CUSTOMERS")
            page = input("Page number (default 1): ").strip() or "1"
            per_page = input("Items per page (default 10): ").strip() or "10"
            
            customers = client.get_customers(int(page), int(per_page))
            for customer in customers:
                print(f"ID: {customer['id']}, Name: {customer['first_name']} {customer['last_name']}, Email: {customer['email']}")
        
        elif choice == '3':
            print("\n👤 GET CUSTOMER")
            customer_id = input("Customer ID: ").strip()
            if customer_id.isdigit():
                customer = client.get_customer(int(customer_id))
                if customer:
                    print(json.dumps(customer, indent=2))
        
        elif choice == '4':
            print("\n✏️ UPDATE CUSTOMER")
            customer_id = input("Customer ID: ").strip()
            if customer_id.isdigit():
                print("Enter new values (leave blank to keep current):")
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                address = input("Address: ").strip()
                
                update_data = {}
                if first_name:
                    update_data["first_name"] = first_name
                if last_name:
                    update_data["last_name"] = last_name
                if email:
                    update_data["email"] = email
                if phone:
                    update_data["phone"] = phone
                if address:
                    update_data["address"] = address
                
                if update_data:
                    client.update_customer(int(customer_id), update_data)
        
        elif choice == '5':
            print("\n🗑️ DELETE CUSTOMER")
            customer_id = input("Customer ID: ").strip()
            if customer_id.isdigit():
                confirm = input(f"Are you sure you want to delete customer {customer_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.delete_customer(int(customer_id))
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def mechanic_menu(client: MechanicAPIClient):
    """Handle mechanic operations."""
    while True:
        print("\n🔧 MECHANIC OPERATIONS")
        print("1. Create Mechanic")
        print("2. List Mechanics")
        print("3. Get Mechanic by ID")
        print("4. Update Mechanic")
        print("5. Delete Mechanic")
        print("6. Mechanics by Workload")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n📝 CREATE MECHANIC")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone (optional): ").strip()
            specialty = input("Specialty (optional): ").strip()
            hourly_rate = input("Hourly Rate (optional): ").strip()
            hire_date = input("Hire Date (YYYY-MM-DD, optional): ").strip()
            
            mechanic_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
            if phone:
                mechanic_data["phone"] = phone
            if specialty:
                mechanic_data["specialty"] = specialty
            if hourly_rate:
                try:
                    mechanic_data["hourly_rate"] = float(hourly_rate)
                except ValueError:
                    print("❌ Invalid hourly rate")
                    continue
            if hire_date:
                mechanic_data["hire_date"] = hire_date
            
            result = client.create_mechanic(mechanic_data)
            if result:
                print(f"Mechanic ID: {result.get('id')}")
        
        elif choice == '2':
            print("\n📋 LIST MECHANICS")
            mechanics = client.get_mechanics()
            for mechanic in mechanics:
                print(f"ID: {mechanic['id']}, Name: {mechanic['first_name']} {mechanic['last_name']}, Specialty: {mechanic.get('specialty', 'N/A')}")
        
        elif choice == '3':
            print("\n🔧 GET MECHANIC")
            mechanic_id = input("Mechanic ID: ").strip()
            if mechanic_id.isdigit():
                mechanic = client.get_mechanic(int(mechanic_id))
                if mechanic:
                    print(json.dumps(mechanic, indent=2))
        
        elif choice == '4':
            print("\n✏️ UPDATE MECHANIC")
            mechanic_id = input("Mechanic ID: ").strip()
            if mechanic_id.isdigit():
                print("Enter new values (leave blank to keep current):")
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                specialty = input("Specialty: ").strip()
                hourly_rate = input("Hourly Rate: ").strip()
                
                update_data = {}
                if first_name:
                    update_data["first_name"] = first_name
                if last_name:
                    update_data["last_name"] = last_name
                if email:
                    update_data["email"] = email
                if phone:
                    update_data["phone"] = phone
                if specialty:
                    update_data["specialty"] = specialty
                if hourly_rate:
                    try:
                        update_data["hourly_rate"] = float(hourly_rate)
                    except ValueError:
                        print("❌ Invalid hourly rate")
                        continue
                
                if update_data:
                    client.update_mechanic(int(mechanic_id), update_data)
        
        elif choice == '5':
            print("\n🗑️ DELETE MECHANIC")
            mechanic_id = input("Mechanic ID: ").strip()
            if mechanic_id.isdigit():
                confirm = input(f"Are you sure you want to delete mechanic {mechanic_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.delete_mechanic(int(mechanic_id))
        
        elif choice == '6':
            print("\n📊 MECHANICS BY WORKLOAD")
            mechanics = client.get_mechanics_by_workload()
            for mechanic in mechanics:
                ticket_count = mechanic.get('ticket_count', 0)
                print(f"ID: {mechanic['id']}, Name: {mechanic['first_name']} {mechanic['last_name']}, Tickets: {ticket_count}")
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def inventory_menu(client: MechanicAPIClient):
    """Handle inventory operations."""
    while True:
        print("\n📦 INVENTORY OPERATIONS")
        print("1. Create Inventory Item")
        print("2. List Inventory")
        print("3. Get Inventory Item by ID")
        print("4. Update Inventory Item")
        print("5. Delete Inventory Item")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n📝 CREATE INVENTORY ITEM")
            if not client.token:
                print("❌ Authentication required for this operation!")
                continue
                
            name = input("Item Name: ").strip()
            price = input("Price: ").strip()
            
            if not name or not price:
                print("❌ Name and price are required!")
                continue
                
            try:
                item_data = {
                    "name": name,
                    "price": float(price)
                }
                result = client.create_inventory_item(item_data)
                if result:
                    print(f"Inventory Item ID: {result.get('id')}")
            except ValueError:
                print("❌ Invalid price!")
        
        elif choice == '2':
            print("\n📋 LIST INVENTORY")
            inventory = client.get_inventory()
            for item in inventory:
                print(f"ID: {item['id']}, Name: {item['name']}, Price: ${item['price']:.2f}")
        
        elif choice == '3':
            print("\n📦 GET INVENTORY ITEM")
            item_id = input("Item ID: ").strip()
            if item_id.isdigit():
                item = client.get_inventory_item(int(item_id))
                if item:
                    print(json.dumps(item, indent=2))
        
        elif choice == '4':
            print("\n✏️ UPDATE INVENTORY ITEM")
            if not client.token:
                print("❌ Authentication required for this operation!")
                continue
                
            item_id = input("Item ID: ").strip()
            if item_id.isdigit():
                print("Enter new values (leave blank to keep current):")
                name = input("Name: ").strip()
                price = input("Price: ").strip()
                
                update_data = {}
                if name:
                    update_data["name"] = name
                if price:
                    try:
                        update_data["price"] = float(price)
                    except ValueError:
                        print("❌ Invalid price!")
                        continue
                
                if update_data:
                    client.update_inventory_item(int(item_id), update_data)
        
        elif choice == '5':
            print("\n🗑️ DELETE INVENTORY ITEM")
            if not client.token:
                print("❌ Authentication required for this operation!")
                continue
                
            item_id = input("Item ID: ").strip()
            if item_id.isdigit():
                confirm = input(f"Are you sure you want to delete item {item_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.delete_inventory_item(int(item_id))
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def service_ticket_menu(client: MechanicAPIClient):
    """Handle service ticket operations."""
    while True:
        print("\n🎫 SERVICE TICKET OPERATIONS")
        print("1. Create Service Ticket")
        print("2. List Service Tickets")
        print("3. Get Service Ticket by ID")
        print("4. Update Service Ticket")
        print("5. Delete Service Ticket")
        print("6. Assign Mechanic to Ticket")
        print("7. Remove Mechanic from Ticket")
        print("8. Bulk Edit Ticket Mechanics")
        print("9. Get Customer Tickets")
        print("10. Get Mechanic Tickets")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n📝 CREATE SERVICE TICKET")
            customer_id = input("Customer ID: ").strip()
            description = input("Description: ").strip()
            vehicle_year = input("Vehicle Year (optional): ").strip()
            vehicle_make = input("Vehicle Make (optional): ").strip()
            vehicle_model = input("Vehicle Model (optional): ").strip()
            vehicle_vin = input("Vehicle VIN (optional): ").strip()
            estimated_cost = input("Estimated Cost (optional): ").strip()
            
            if not customer_id.isdigit() or not description:
                print("❌ Customer ID and description are required!")
                continue
            
            ticket_data = {
                "customer_id": int(customer_id),
                "description": description
            }
            
            if vehicle_year and vehicle_year.isdigit():
                ticket_data["vehicle_year"] = int(vehicle_year)
            if vehicle_make:
                ticket_data["vehicle_make"] = vehicle_make
            if vehicle_model:
                ticket_data["vehicle_model"] = vehicle_model
            if vehicle_vin:
                ticket_data["vehicle_vin"] = vehicle_vin
            if estimated_cost:
                try:
                    ticket_data["estimated_cost"] = float(estimated_cost)
                except ValueError:
                    print("❌ Invalid estimated cost!")
                    continue
            
            result = client.create_service_ticket(ticket_data)
            if result:
                print(f"Service Ticket ID: {result.get('id')}")
        
        elif choice == '2':
            print("\n📋 LIST SERVICE TICKETS")
            tickets = client.get_service_tickets()
            for ticket in tickets:
                print(f"ID: {ticket['id']}, Customer: {ticket.get('customer_id')}, Status: {ticket.get('status', 'Open')}")
        
        elif choice == '3':
            print("\n🎫 GET SERVICE TICKET")
            ticket_id = input("Ticket ID: ").strip()
            if ticket_id.isdigit():
                ticket = client.get_service_ticket(int(ticket_id))
                if ticket:
                    print(json.dumps(ticket, indent=2))
        
        elif choice == '4':
            print("\n✏️ UPDATE SERVICE TICKET")
            ticket_id = input("Ticket ID: ").strip()
            if ticket_id.isdigit():
                print("Enter new values (leave blank to keep current):")
                description = input("Description: ").strip()
                status = input("Status (Open/In Progress/Completed/Cancelled): ").strip()
                estimated_cost = input("Estimated Cost: ").strip()
                actual_cost = input("Actual Cost: ").strip()
                
                update_data = {}
                if description:
                    update_data["description"] = description
                if status:
                    update_data["status"] = status
                if estimated_cost:
                    try:
                        update_data["estimated_cost"] = float(estimated_cost)
                    except ValueError:
                        print("❌ Invalid estimated cost!")
                        continue
                if actual_cost:
                    try:
                        update_data["actual_cost"] = float(actual_cost)
                    except ValueError:
                        print("❌ Invalid actual cost!")
                        continue
                
                if update_data:
                    client.update_service_ticket(int(ticket_id), update_data)
        
        elif choice == '5':
            print("\n🗑️ DELETE SERVICE TICKET")
            ticket_id = input("Ticket ID: ").strip()
            if ticket_id.isdigit():
                confirm = input(f"Are you sure you want to delete ticket {ticket_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    client.delete_service_ticket(int(ticket_id))
        
        elif choice == '6':
            print("\n👨‍🔧 ASSIGN MECHANIC TO TICKET")
            ticket_id = input("Ticket ID: ").strip()
            mechanic_id = input("Mechanic ID: ").strip()
            if ticket_id.isdigit() and mechanic_id.isdigit():
                client.assign_mechanic_to_ticket(int(ticket_id), int(mechanic_id))
        
        elif choice == '7':
            print("\n❌ REMOVE MECHANIC FROM TICKET")
            ticket_id = input("Ticket ID: ").strip()
            mechanic_id = input("Mechanic ID: ").strip()
            if ticket_id.isdigit() and mechanic_id.isdigit():
                client.remove_mechanic_from_ticket(int(ticket_id), int(mechanic_id))
        
        elif choice == '8':
            print("\n🔄 BULK EDIT TICKET MECHANICS")
            ticket_id = input("Ticket ID: ").strip()
            if ticket_id.isdigit():
                add_ids_str = input("Mechanic IDs to add (comma-separated): ").strip()
                remove_ids_str = input("Mechanic IDs to remove (comma-separated): ").strip()
                
                add_ids = []
                remove_ids = []
                
                if add_ids_str:
                    try:
                        add_ids = [int(x.strip()) for x in add_ids_str.split(',') if x.strip()]
                    except ValueError:
                        print("❌ Invalid mechanic IDs to add!")
                        continue
                
                if remove_ids_str:
                    try:
                        remove_ids = [int(x.strip()) for x in remove_ids_str.split(',') if x.strip()]
                    except ValueError:
                        print("❌ Invalid mechanic IDs to remove!")
                        continue
                
                client.bulk_edit_ticket_mechanics(int(ticket_id), add_ids, remove_ids)
        
        elif choice == '9':
            print("\n👤 GET CUSTOMER TICKETS")
            customer_id = input("Customer ID: ").strip()
            if customer_id.isdigit():
                tickets = client.get_customer_tickets(int(customer_id))
                for ticket in tickets:
                    print(f"ID: {ticket['id']}, Description: {ticket['description']}, Status: {ticket.get('status', 'Open')}")
        
        elif choice == '10':
            print("\n🔧 GET MECHANIC TICKETS")
            mechanic_id = input("Mechanic ID: ").strip()
            if mechanic_id.isdigit():
                tickets = client.get_mechanic_tickets(int(mechanic_id))
                for ticket in tickets:
                    print(f"ID: {ticket['id']}, Description: {ticket['description']}, Status: {ticket.get('status', 'Open')}")
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def auth_menu(client: MechanicAPIClient):
    """Handle authentication operations."""
    while True:
        print("\n🔐 AUTHENTICATION")
        print(f"Status: {'✅ Logged in' if client.token else '❌ Not logged in'}")
        if client.token:
            print(f"Customer ID: {client.authenticated_customer_id}")
        print("\n1. Login")
        print("2. Logout")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n🔐 LOGIN")
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if email and password:
                client.login_customer(email, password)
            else:
                print("❌ Email and password are required!")
        
        elif choice == '2':
            print("\n🔓 LOGOUT")
            client.clear_auth_token()
            print("✅ Logged out successfully!")
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def reports_menu(client: MechanicAPIClient):
    """Handle reports and analytics."""
    while True:
        print("\n📊 REPORTS & ANALYTICS")
        print("1. Mechanics by Workload")
        print("2. Customer Summary")
        print("3. Inventory Summary")
        print("4. Service Ticket Summary")
        print("0. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            print("\n📊 MECHANICS BY WORKLOAD")
            mechanics = client.get_mechanics_by_workload()
            if mechanics:
                print(f"{'ID':<5} {'Name':<25} {'Specialty':<20} {'Tickets':<8}")
                print("-" * 60)
                for mechanic in mechanics:
                    name = f"{mechanic['first_name']} {mechanic['last_name']}"
                    specialty = mechanic.get('specialty', 'N/A')[:19]
                    ticket_count = mechanic.get('ticket_count', 0)
                    print(f"{mechanic['id']:<5} {name:<25} {specialty:<20} {ticket_count:<8}")
        
        elif choice == '2':
            print("\n👥 CUSTOMER SUMMARY")
            customers = client.get_customers(1, 100)  # Get first 100 customers
            print(f"Total Customers: {len(customers)}")
            if customers:
                print(f"{'ID':<5} {'Name':<25} {'Email':<30}")
                print("-" * 62)
                for customer in customers[:10]:  # Show first 10
                    name = f"{customer['first_name']} {customer['last_name']}"
                    email = customer['email'][:29]
                    print(f"{customer['id']:<5} {name:<25} {email:<30}")
                if len(customers) > 10:
                    print(f"... and {len(customers) - 10} more")
        
        elif choice == '3':
            print("\n📦 INVENTORY SUMMARY")
            inventory = client.get_inventory()
            if inventory:
                total_value = sum(item['price'] for item in inventory)
                print(f"Total Items: {len(inventory)}")
                print(f"Total Value: ${total_value:.2f}")
                print(f"{'ID':<5} {'Name':<30} {'Price':<10}")
                print("-" * 47)
                for item in inventory[:10]:  # Show first 10
                    name = item['name'][:29]
                    price = f"${item['price']:.2f}"
                    print(f"{item['id']:<5} {name:<30} {price:<10}")
                if len(inventory) > 10:
                    print(f"... and {len(inventory) - 10} more items")
        
        elif choice == '4':
            print("\n🎫 SERVICE TICKET SUMMARY")
            tickets = client.get_service_tickets()
            if tickets:
                status_counts = {}
                for ticket in tickets:
                    status = ticket.get('status', 'Open')
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                print(f"Total Tickets: {len(tickets)}")
                print("\nStatus Breakdown:")
                for status, count in status_counts.items():
                    print(f"  {status}: {count}")
                
                print(f"\n{'ID':<5} {'Customer':<12} {'Status':<15} {'Description':<30}")
                print("-" * 64)
                for ticket in tickets[:10]:  # Show first 10
                    customer_id = ticket.get('customer_id', 'N/A')
                    status = ticket.get('status', 'Open')
                    description = ticket['description'][:29]
                    print(f"{ticket['id']:<5} {customer_id:<12} {status:<15} {description:<30}")
                if len(tickets) > 10:
                    print(f"... and {len(tickets) - 10} more tickets")
        
        elif choice == '0':
            break
        else:
            print("❌ Invalid option!")


def main():
    """Main CLI interface."""
    print("🔧 Welcome to the Mechanic Shop API Client!")
    print("Make sure your Flask API server is running on http://127.0.0.1:5000")
    
    # Initialize client
    client = MechanicAPIClient()
    
    # Test connection with a simple endpoint first
    try:
        # Try a simple inventory endpoint first (usually works even with empty DB)
        response = client._make_request('GET', '/inventory/')
        if response.status_code in [200, 404]:
            print("✅ Connected to API server successfully!")
        elif response.status_code == 500:
            print("⚠️  API server connected but returned internal error")
            print("This might be due to database issues - trying to continue...")
        else:
            print(f"⚠️  API server responded with status {response.status_code}")
            print("Trying to continue anyway...")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server!")
        print("Make sure the Flask application is running on http://127.0.0.1:5000")
        return
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        print("Trying to continue anyway...")
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            customer_menu(client)
        elif choice == '2':
            mechanic_menu(client)
        elif choice == '3':
            inventory_menu(client)
        elif choice == '4':
            service_ticket_menu(client)
        elif choice == '5':
            auth_menu(client)
        elif choice == '6':
            reports_menu(client)
        elif choice == '0':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option! Please try again.")


if __name__ == "__main__":
    main()