from flask import Flask
from flask import render_template
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def home():
    group:str = "223з"
    number = 123
    flomber = 10.23
    flomcer = 10.2300000000000000000000001
    is_it = True

    return f"Hello students! Вітаю студентів групи {group} гр!"

@app.route('/about')
def about():
    return "Це наша весела компанія"

# @app.route('/user')
# def user():
#     url_for('static', filename='index.html')


@app.route('/user/<username>')
def profile(username):
    return render_template('hello.html', person=username)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    return jsonify(data)

# @app.route('/api/add', methods=['POST'])
# def add_data():
#     data = request.get_json()
#     return jsonify({"received": data}), 201


if __name__ == "__main__":
    app.run(debug=True, port=80)  # By default, it runs on localhost:5000