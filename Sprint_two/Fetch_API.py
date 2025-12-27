import requests

def fetch_current_ip():
    endpoint = "https://api.ipify.org?format=json"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_joke():
    endpoint = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            print(data["setup"])
            print("Press Enter to see the punchline...")
            input()
            print(data["punchline"])
        else:
            print(f"Error: Received status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Fetching current IP address:")
    fetch_current_ip()
    print("\nFetching a random joke:")
    fetch_joke()