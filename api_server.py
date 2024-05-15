from flask import Flask, request, jsonify, render_template
import logging
from logging.handlers import RotatingFileHandler
import os

# 로깅 설정
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(handler)

app = Flask(__name__)

# 주문 목록을 저장할 리스트
orders = []

@app.route('/api/orders', methods=['POST'])
def create_or_receive_order():
    order_data = request.json
    orders.append(order_data)
    logger.info(f"New order added: {order_data}")
    return jsonify({'status': 'success', 'order': order_data}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    if request.args.get('format') == 'json':
        return jsonify({'status': 'success', 'orders': orders}), 200
    return render_template('orders.html', orders=orders)

@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"404 Not Found: {request.url}")
    return jsonify({'error': 'Not Found', 'status': 404}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 Internal Server Error: {request.url}")
    return jsonify({'error': 'Internal Server Error', 'status': 500}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
