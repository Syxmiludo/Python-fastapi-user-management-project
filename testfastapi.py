import requests

BASE_URL = "http://127.0.0.1:8000"

# --- 1. Create a user ---
user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "password": "password123",
    "email": "john.doe@example.com",
    "phone_number": "1234567890"
}

print("=== Creating User ===")
response = requests.post(f"{BASE_URL}/users", json=user_data)
try:
    print(response.status_code, response.json(), "\n")
except Exception:
    print(response.status_code, response.text, "\n")

# --- 2. Get the user ---
print("=== Getting User ===")
response = requests.get(f"{BASE_URL}/get_user", params={"username": "johndoe"})
try:
    print(response.status_code, response.json(), "\n")
except Exception:
    print(response.status_code, response.text, "\n")

# --- 3. Login ---
login_data = {
    "username": "johndoe",
    "password": "password123"
}

print("=== Logging in ===")
response = requests.post(f"{BASE_URL}/login", data=login_data)
try:
    print(response.status_code, response.json(), "\n")
except Exception:
    print(response.status_code, response.text, "\n")

# --- 4. Update the user ---
update_data = {
    "first_name": "Johnny",
    "last_name": "Doe",
    "password": "newpassword123",
    "email": "johnny.doe@example.com",
    "phone_number": "0987654321"
}

print("=== Updating User ===")
response = requests.put(f"{BASE_URL}/users/johndoe", json=update_data)
try:
    print(response.status_code, response.json(), "\n")
except Exception:
    print(response.status_code, response.text, "\n")

# --- 5. Delete the user ---
print("=== Deleting User ===")
response = requests.delete(f"{BASE_URL}/users/johndoe")
try:
    print(response.status_code, response.json(), "\n")
except Exception:
    print(response.status_code, response.text, "\n")
