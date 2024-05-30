from flask import Flask, jsonify
import requests

app = Flask(__name__)

WINDOW_SIZE = 10
numbers_window = []

# Base URL of the test server
BASE_URL = "http://20.244.56.144/test"

# Function to fetch numbers from the test server API
def fetch_numbers(numberid):
    endpoints = {
        'p': 'primes',
        'f': 'fibo',  # Assuming 'fibo' is the correct endpoint for Fibonacci numbers
        'e': 'even',
 'r': 'random'
    }

    if numberid not in endpoints:
        return []

    url = f"{BASE_URL}/{endpoints[numberid]}"
    try:
        response = requests.get(url, timeout=0.5)  # 500 ms timeout
        response.raise_for_status()
        return response.json().get('numbers', [])
    except (requests.RequestException, ValueError):
        return []

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    window_prev_state = list(numbers_window)  # Copy current state of window
    new_numbers = fetch_numbers(numberid)

    # Add new numbers to the window, ensuring uniqueness and no duplicates
    for number in new_numbers:
        if number not in numbers_window:
            numbers_window.append(number)

    # Limit the window to the specified size
    while len(numbers_window) > WINDOW_SIZE:
        numbers_window.pop(0)  # Remove the oldest number

    window_curr_state = list(numbers_window)

    # Calculate the average of the numbers in the window
    if numbers_window:
        avg = sum(numbers_window) / len(numbers_window)
    else:
        avg = 0.0
    
    response = {
    "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '_main_':
    app.run(debug=True,port=9876)

