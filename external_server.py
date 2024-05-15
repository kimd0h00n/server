from flask import Flask, request, jsonify, render_template
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# 주문 목록을 저장할 리스트
orders = []

@app.route('/api/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    if not order_data:
        logging.error("No data provided")
        return jsonify({'error': 'No data provided'}), 400

    orders.append(order_data)
    logging.info(f"New order added: {order_data}")
    return jsonify({'status': 'success', 'order': order_data}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({'status': 'success', 'orders': orders}), 200

@app.errorhandler(404)
def page_not_found(error):
    logging.error(f"404 Not Found: {request.url}")
    return jsonify({'error': 'Not Found', 'status': 404}), 404

@app.errorhandler(500)
def internal_server_error(error):
    logging.error(f"500 Internal Server Error: {request.url}, Error: {error}")
    return jsonify({'error': 'Internal Server Error', 'status': 500}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Default port 5000
    app.run(host='0.0.0.0', port=port, debug=False)
