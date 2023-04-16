from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
@app.route('/convert', methods=['GET'])
def convert_currency():
    base_currency = request.args.get('base')
    target_currency = request.args.get('target')
    amount = request.args.get('amount')

    if not base_currency or not target_currency or not amount:
        return jsonify({'error': 'Invalid parameters'})

    response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_currency.upper()}')
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve exchange rates'})

    exchange_rates = response.json().get('rates')
    if not exchange_rates:
        return jsonify({'error': 'Exchange rates not available'})

    if target_currency.upper() not in exchange_rates:
        return jsonify({'error': f'Unsupported target currency: {target_currency}'})

    exchange_rate = exchange_rates[target_currency.upper()]
    converted_amount = float(amount) * exchange_rate

    return jsonify({'result': round(converted_amount, 2)})

if __name__ == '__main__':
    app.run()
