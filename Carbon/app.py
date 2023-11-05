from hashlib import sha256
import json
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, send_file,jsonify
import io

# Define the Block and Blockchain classes as before
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.carbon_footprint_data = []

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def add_carbon_footprint_data(self, data):
        self.carbon_footprint_data.append(data)

# Initialize the Flask app
app = Flask(__name__)
blockchain = Blockchain()

# Define the routes for the application
@app.route('/')
def display_chain():
    reversed_chain = list(reversed(blockchain.chain))
    return render_template('index.html', chain=reversed_chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            data = int(request.form['data'])
        except ValueError as e:
            # Handle the ValueError here
            return render_template('value_error.html', error=str(e))

        index = len(blockchain.chain)
        new_block = Block(index, time.time(), data, blockchain.get_latest_block().hash)
        blockchain.add_block(new_block)
        blockchain.add_carbon_footprint_data(data)
        return display_chain()


@app.route('/carbon_footprint_calculator', methods=['GET', 'POST'])
def carbon_footprint_calculator():
    if request.method == 'POST':
        try:
            electricity_bill = int(request.form['electric_bill'])
            gas_bill = int(request.form['gas_bill'])
            oil_bill = int(request.form['oil_bill'])
            car_mileage = int(request.form['car_mileage'])
            short_flights = int(request.form['short_flights'])
            long_flights = int(request.form['long_flights'])

            total_carbon_footprint = (
                (electricity_bill * 105) +
                (gas_bill * 105) +
                (oil_bill * 113) +
                (car_mileage * 0.79) +
                (short_flights * 1100) +
                (long_flights * 4400) 
            )

            return render_template('carbon_footprint_calculator.html', result=total_carbon_footprint)

        except ValueError as e:
            # Handle the ValueError here
            return render_template('value_error.html', error=str(e))

    return render_template('carbon_footprint_calculator.html')

@app.route('/graph')
def display_graph():
    cumulative_data = [0]
    years = [0]

    for i in range(1, len(blockchain.carbon_footprint_data)):
        cumulative_data.append(cumulative_data[i-1] + blockchain.carbon_footprint_data[i])
        years.append(i)

    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(years, cumulative_data, marker='o')
    plt.title('Environmental Impact of Cumulative Carbon Footprint Over Time ')
    plt.xlabel('Years')
    plt.ylabel('Cumulative Carbon Footprint Data')

    # Check if the graph hits 12 and trigger a message
    alert_message = None
    if any(data >= 100 for data in cumulative_data):
        alert_message = "The carbon footprint data has reached above critical point(100)."
        plt.text(max(years) * 0.9, max(cumulative_data) * 0.9, alert_message, fontsize=12, ha='right', va='center')

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust the spacing as needed

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
