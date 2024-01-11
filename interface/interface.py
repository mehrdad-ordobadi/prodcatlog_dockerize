from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_item', methods=['GET', 'POST'])
def get_item():
    item = None
    if request.method == 'POST':
        name = request.form['name']
        response = requests.get(f"http://app:5001/item/{name}")
        if response.status_code == 200:
            item = response.json()
    return render_template('get_item.html', item=item)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        response = requests.post("http://app:5001/item", json={"name": name})
        return jsonify(response.json())
    return render_template('add_item.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
