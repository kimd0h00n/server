from flask import Flask, request, jsonify
import os
import logging

# 로거 설정
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/api/orders', methods=['POST'])
def receive_order():
    data = request.get_json()

    # 주문 데이터 처리 (여기서는 단순히 로깅)
    items = data.get('items', [])
    total = data.get('total', 0)

    logging.info("Received order:")
    for item in items:
        logging.info(f"Item: {item['name']}, Price: {item['price']}")
    logging.info(f"Total: {total}")
    
    # 응답 생성
    response = {
        "status": "success",
        "message": "Order received",
        "received_items": items,
        "received_total": total
    }
    
    return jsonify(response), 200

@app.errorhandler(404)
def not_found(error):
    logging.error(f"404 Not Found: {request.url}")
    return jsonify({"error": "Not Found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 Internal Server Error: {request.url}")
    return jsonify({"error": "Internal Server Error", "status": 500}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
