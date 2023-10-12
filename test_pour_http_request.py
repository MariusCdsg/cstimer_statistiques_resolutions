import time

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data/<param1>/<param2>', methods=['GET'])
def get_data(param1, param2):
    # You can now use param1 and param2 as parameters in your function
    data = {
        'param1': param1,
        'param2': param2
    }
    return jsonify(data)
with app.test_request_context():
    print("yo")
    time.sleep(1)
    get_data("hello test", "prout")
# get_data("hello test")
if __name__ == '__main__':
    app.run(debug=True)
