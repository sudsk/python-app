import socket
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    return jsonify({
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname()),
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'Hello World',
    })

@app.route('/api/v1/healthz')
def healthz():
    return jsonify({
        'status': 'ok'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
