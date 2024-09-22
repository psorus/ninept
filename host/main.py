from flask import Flask, request, jsonify
import threading
import queue
import time  # Simulate long processing with sleep

# Initialize Flask app
app = Flask(__name__)

# Create a queue to handle requests one at a time
request_queue = queue.Queue()

# Cache for storing previous request results
cache = {}

# Sample function that simulates a time-consuming task
def time_consuming_function(str1, str2):
    # Simulate processing time
    time.sleep(5)
    return str1 + " " + str2

# Worker function to process requests from the queue
def worker():
    while True:
        # Get a request from the queue
        str1, str2, result_event, result_store = request_queue.get()

        # Check if the request result is already cached
        if (str1, str2) in cache:
            result_store['result'] = cache[(str1, str2)]
        else:
            # Call the time-consuming function
            result = time_consuming_function(str1, str2)
            # Store the result in cache
            cache[(str1, str2)] = result
            result_store['result'] = result

        # Notify that the result is ready
        result_event.set()

        # Mark the task as done
        request_queue.task_done()

# Start the worker thread
threading.Thread(target=worker, daemon=True).start()

# Define a route to accept POST requests with two string inputs
@app.route('/combine', methods=['POST'])
def combine():
    # Get JSON data from the request
    data = request.get_json()
    str1 = data.get('str1', '')
    str2 = data.get('str2', '')

    # Create an event to wait for the result and a dict to store the result
    result_event = threading.Event()
    result_store = {}

    # Add the request to the queue
    request_queue.put((str1, str2, result_event, result_store))

    # Wait until the result is ready
    result_event.wait()

    # Return the result as JSON
    return jsonify({'result': result_store['result']})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

