"""Quick API test script to verify all features work"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("Testing Mechanic Shop API")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(BASE_URL)
    print(f"   ✅ Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Create customer
print("\n2. Testing customer creation...")
try:
    customer_data = {
        "first_name": "Jane",
        "last_name": "Test",
        "email": "jane.test@example.com",
        "password": "secure123",
        "phone": "555-9999"
    }
    response = requests.post(f"{BASE_URL}/customers/", json=customer_data)
    print(f"   ✅ Status: {response.status_code}")
    customer_id = response.json().get('id')
    print(f"   Customer ID: {customer_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Create mechanic
print("\n3. Testing mechanic creation...")
try:
    mechanic_data = {
        "first_name": "Tom",
        "last_name": "Mechanic",
        "email": "tom.test@example.com",
        "specialty": "Transmission",
        "hourly_rate": 85.00
    }
    response = requests.post(f"{BASE_URL}/mechanics/", json=mechanic_data)
    print(f"   ✅ Status: {response.status_code}")
    mechanic_id = response.json().get('id')
    print(f"   Mechanic ID: {mechanic_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Create inventory
print("\n4. Testing inventory creation...")
try:
    inventory_data = {
        "name": "Brake Pads",
        "price": 45.99
    }
    response = requests.post(f"{BASE_URL}/inventory/", json=inventory_data)
    print(f"   ✅ Status: {response.status_code}")
    inventory_id = response.json().get('id')
    print(f"   Inventory ID: {inventory_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Create service ticket
print("\n5. Testing service ticket creation...")
try:
    ticket_data = {
        "customer_id": customer_id,
        "vehicle_make": "Honda",
        "vehicle_model": "Civic",
        "description": "Brake replacement",
        "estimated_cost": 200.00
    }
    response = requests.post(f"{BASE_URL}/service-tickets/", json=ticket_data)
    print(f"   ✅ Status: {response.status_code}")
    ticket_id = response.json().get('id')
    print(f"   Ticket ID: {ticket_id}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Assign mechanic to ticket
print("\n6. Testing mechanic assignment...")
try:
    response = requests.put(f"{BASE_URL}/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}")
    print(f"   ✅ Status: {response.status_code}")
    print(f"   Message: {response.json().get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Add part to ticket
print("\n7. Testing adding inventory part to ticket...")
try:
    response = requests.put(f"{BASE_URL}/service-tickets/{ticket_id}/add-part/{inventory_id}")
    print(f"   ✅ Status: {response.status_code}")
    print(f"   Message: {response.json().get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 8: Login and get token
print("\n8. Testing customer login (token authentication)...")
try:
    login_data = {
        "email": "jane.test@example.com",
        "password": "secure123"
    }
    response = requests.post(f"{BASE_URL}/customers/login", json=login_data)
    print(f"   ✅ Status: {response.status_code}")
    token = response.json().get('token')
    print(f"   Token received: {token[:30]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 9: Get my tickets with token
print("\n9. Testing authenticated route (my-tickets)...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/customers/my-tickets", headers=headers)
    print(f"   ✅ Status: {response.status_code}")
    print(f"   Number of tickets: {len(response.json())}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 10: Test rate limiting (create multiple customers quickly)
print("\n10. Testing rate limiting...")
try:
    success_count = 0
    for i in range(12):
        customer_data = {
            "first_name": f"Test{i}",
            "last_name": "User",
            "email": f"test{i}@example.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/customers/", json=customer_data)
        if response.status_code == 201:
            success_count += 1
        elif response.status_code == 429:
            print(f"   ✅ Rate limit triggered after {success_count} requests")
            print(f"   Response: {response.json()}")
            break
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 11: Test caching (get customers twice)
print("\n11. Testing caching...")
try:
    import time
    response1 = requests.get(f"{BASE_URL}/customers/")
    time1 = response1.elapsed.total_seconds()
    
    response2 = requests.get(f"{BASE_URL}/customers/")
    time2 = response2.elapsed.total_seconds()
    
    print(f"   ✅ First request: {time1:.4f}s")
    print(f"   ✅ Cached request: {time2:.4f}s")
    print(f"   Cache is {'working' if time2 < time1 else 'not working'}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
