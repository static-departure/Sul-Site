from flask import Flask, render_template, request, jsonify
from intasend import APIService
import os

app = Flask(__name__)

# Set your API token and publishable key as environment variables
TOKEN = os.getenv("INTASEND_API_TOKEN")  # Set your API token in the environment
PUBLISHABLE_KEY = os.getenv("INTASEND_PUBLISHABLE_KEY")  # Set your publishable key in the environment

# Initialize the IntaSend APIService
service = APIService(token=TOKEN, publishable_key=PUBLISHABLE_KEY)

# Route to display the payment form
@app.route('/')
def home():
    return render_template('payment_form.html')

# Route to handle form submission and initiate STK push
@app.route('/pay', methods=['POST'])
def initiate_stk_push():
    try:
        # Collect data from the form
        phone_number = request.form['phone_number']
        email = request.form['email']
        amount = float(request.form['amount'])  # Convert amount to float
        narrative = "Purchase"  # Set the narrative for the transaction

        # Prepare and send the STK Push request
        response = service.collect.mpesa_stk_push(
            phone_number=phone_number,
            email=email,
            amount=amount,
            narrative=narrative
        )

        # Return the response JSON to the user
        return jsonify({"message": "STK Push initiated successfully!", "details": response})

    except Exception as e:
        # Catch all exceptions and return an error message
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)
