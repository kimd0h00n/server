from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route('/api/orders', methods=['POST'])
def receive_order():
    data = request.get_json()
    items = data.get('items', [])
    total = data.get('total', 0)

    app.logger.info("Received order:")
    for item in items:
        app.logger.info(f"Item: {item['name']}, Price: {item['price']}")
    app.logger.info(f"Total: {total}")
    
    response = {
        "status": "success",
        "message": "Order received",
        "received_items": items,
        "received_total": total
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    # 로깅 설정
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    # 디버그 모드 비활성화
    app.run(debug=False, port=5001)
