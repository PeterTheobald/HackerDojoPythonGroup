from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get_data')
def get_data():
    data = {'message': 'Hello from the server!'}
    return jsonify(data)


@app.route('/api/get_html')
def get_html():
    return render_template('message.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
