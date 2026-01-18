from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    return jsonify({
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
