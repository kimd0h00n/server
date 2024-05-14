from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

class MenuItem:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_total(self):
        return sum(item.price for item in self.items)

menu_items = [
    MenuItem("계란말이", 4000, "egg.jpg"),
    MenuItem("황도", 4500, "hwangdo.jpg"),
    MenuItem("제육볶음", 5500, "jeyouk.jpg"),
    MenuItem("냉동 만두", 4000, "mandoo.jpg"),
    MenuItem("오뎅탕", 4500, "odaeng.jpg"),
    MenuItem("소세지 야채볶음", 5500, "ssoya.jpg")
]

order = Order()

@app.route('/')
def index():
    return render_template('index.html', menu_items=menu_items, total=order.get_total())

@app.route('/order', methods=['POST'])
def order_menu():
    item_index = int(request.form.get('item_index'))
    order.add_item(menu_items[item_index])
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET'])
def checkout():
    total = order.get_total()
    send_order_to_server(order.items, total)  # 서버에 주문 정보 전송
    order.items.clear()
    return render_template('checkout.html', total=total)

def send_order_to_server(items, total):
    api_url = "http://example.com/api/orders"  # 외부 API URL
    headers = {'Content-Type': 'application/json'}
    data = {
        "items": [{"name": item.name, "price": item.price} for item in items],
        "total": total
    }
    response = requests.post(api_url, json=data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == '__main__':
    app.run(debug=True)
