import requests
import os

# Configuration
BASE_URL = "http://localhost:5000/api/register"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'uploads')

def create_dummy_pdf(filename):
    with open(filename, 'wb') as f:
        # Minimal PDF header
        f.write(b'%PDF-1.4\n%EOF')

def test_upload():
    print("Testing License Upload (PDF)...")
    
    # Create dummy PDF
    pdf_file = 'test_license.pdf'
    create_dummy_pdf(pdf_file)
    
    # Data for driver registration
    data = {
        'username': 'driver_pdf_test',
        'password': 'Password123!',
        'role': 'driver',
        'email': 'driver_pdf@example.com',
        'phonenumber': '1234567890',
        'age': '30',
        'licenseid': 'LIC88888'
    }
    
    files = {
        'license_file': open(pdf_file, 'rb')
    }
    
    try:
        # Send request
        response = requests.post(BASE_URL, data=data, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("PASS: Registration successful")
            
            # Verify file saved
            saved_file = os.path.join(UPLOAD_FOLDER, 'test_license.pdf') # secure_filename might change it slightly if special chars but here it's simple
            if os.path.exists(saved_file):
                print(f"PASS: File saved at {saved_file}")
            else:
                print(f"FAIL: File not found at {saved_file}")
                
        else:
            print("FAIL: Registration failed")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        files['license_file'].close()
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

if __name__ == "__main__":
    # Ensure server is running before running this
    test_upload()
