import requests

# Configuration
base_url = ""  # Replace with your APEX app's base URL
login_url = base_url + ""  # URL for login
csrf_test_url = base_url + ""  # URL where you want to test CSRF (like form submission)

# User credentials
username = ""
password = ""

# Start a session to store cookies
session = requests.Session()

# Step 1: Authenticate to the APEX application
def login():
    login_data = {
        "username": username,
        "password": password
    }
    response = session.post(login_url, data=login_data)
    
    # Check if login was successful (status 200, etc.)
    if response.status_code == 200:
        print("Login successful.")
    else:
        print(f"Login failed: {response.status_code}")
        return False
    return True

# Step 2: Fetch a CSRF token (if it's stored in cookies, forms, or headers)
def get_csrf_token():
    response = session.get(csrf_test_url)
    
    # Parse the CSRF token from response (assumes token is in a hidden input field)
    # This needs to be adjusted based on how the app presents CSRF tokens
    if "csrf_token" in response.text:
        csrf_token = extract_csrf_token(response.text)  # You need to implement this part based on the HTML
        return csrf_token
    else:
        print("Could not find CSRF token in the response.")
        return None

# Step 3: Test request with valid CSRF token
def test_with_valid_csrf(csrf_token):
    headers = {
        "X-CSRF-TOKEN": csrf_token  # Adjust this if your app expects the token in headers or form data
    }
    data = {
        "your_form_field": "test_data",
        "csrf_token": csrf_token
    }
    
    response = session.post(csrf_test_url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("Request with valid CSRF token succeeded.")
    else:
        print(f"Request with valid CSRF token failed: {response.status_code}")

# Step 4: Test request with invalid CSRF token
def test_with_invalid_csrf():
    headers = {
        "X-CSRF-TOKEN": "invalid_token"
    }
    data = {
        "your_form_field": "test_data",
        "csrf_token": "invalid_token"
    }
    
    response = session.post(csrf_test_url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("Request with invalid CSRF token succeeded (Potential CSRF Vulnerability).")
    else:
        print(f"Request with invalid CSRF token failed as expected: {response.status_code}")

# Helper function to extract CSRF token from HTML (needs to be implemented based on your app's HTML)
def extract_csrf_token(html):
    # Example of extracting CSRF token using regex or BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Assuming the CSRF token is in a hidden input field named 'csrf_token'
    token_tag = soup.find('input', {'name': 'csrf_token'})
    
    if token_tag:
        return token_tag['value']
    return None

# Main execution flow
def main():
    if login():
        print("Getting CSRF Token")
        csrf_token = get_csrf_token()
        if csrf_token:
            print("Testing tokens")
            test_with_valid_csrf(csrf_token)
            test_with_invalid_csrf()
        else:
            print("No valid CSRF token found to proceed with testing.")

if __name__ == "__main__":
    main()