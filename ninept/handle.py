import requests

def qwen(content: str, role: str) -> str:
    # The URL of your Flask server endpoint
    url = "http://127.0.0.1:5000/combine"

    # The data to send in the POST request
    data = {
        'content': content,
        'role': role
    }

    # Send the POST request and get the response
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the result from the JSON response
        result = response.json().get('result', '')
        return result
    else:
        raise Exception(f"Server error: {response.status_code}")


