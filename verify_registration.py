import os
import json
from app import create_app

def verify_registration():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    print("Running verification tests...")

    # Test 1: Driver Registration with licenseid
    print("\nTest 1: Driver Registration with licenseid")
    driver_data = {
        "email": "driver_verif@example.com",
        "username": "driver_verif",
        "password": "password123",
        "role": "driver",
        "phonenumber": "1234567890",
        "age": 30,
        "licenseid": "LIC12345"
    }
    resp = client.post('/api/register', json=driver_data)
    if resp.status_code == 201:
        print("PASS: Driver registered successfully")
    else:
        print(f"FAIL: Driver registration failed: {resp.json}")

    # Test 2: Passenger Registration with attending_school
    print("\nTest 2: Passenger Registration with attending_school")
    passenger_data = {
        "email": "passenger_verif@example.com",
        "username": "passenger_verif",
        "password": "password123",
        "role": "passenger",
        "phonenumber": "0987654321",
        "age": 20,
        "attending_school": "Pascal High"
    }
    resp = client.post('/api/register', json=passenger_data)
    if resp.status_code == 201:
        print("PASS: Passenger registered successfully")
    else:
        print(f"FAIL: Passenger registration failed: {resp.json}")

    # Test 3: Driver Missing licenseid
    print("\nTest 3: Driver Missing licenseid")
    driver_fail_data = driver_data.copy()
    del driver_fail_data['licenseid']
    driver_fail_data['email'] = "driver_fail@example.com"
    driver_fail_data['username'] = "driver_fail"
    resp = client.post('/api/register', json=driver_fail_data)
    if resp.status_code == 400 and "License ID is required" in resp.json.get('error', ''):
        print("PASS: Driver missing licenseid rejected correctly")
    else:
        print(f"FAIL: Driver missing licenseid not rejected correctly: {resp.status_code} {resp.json}")

    # Test 4: Passenger Missing attending_school
    print("\nTest 4: Passenger Missing attending_school")
    passenger_fail_data = passenger_data.copy()
    del passenger_fail_data['attending_school']
    passenger_fail_data['email'] = "passenger_fail@example.com"
    passenger_fail_data['username'] = "passenger_fail"
    resp = client.post('/api/register', json=passenger_fail_data)
    if resp.status_code == 400 and "Attending school is required" in resp.json.get('error', ''):
        print("PASS: Passenger missing attending_school rejected correctly")
    else:
        print(f"FAIL: Passenger missing attending_school not rejected correctly: {resp.status_code} {resp.json}")

    # Cleanup
    if os.path.exists('test_drivers.json'):
        os.remove('test_drivers.json')
    if os.path.exists('test_passengers.json'):
        os.remove('test_passengers.json')

if __name__ == "__main__":
    verify_registration()
