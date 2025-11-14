from flask import Flask, render_template, request
import socket
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Get server's hostname
    hostname = socket.gethostname()

    # Get server's local IP
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "Unable to determine"

    # Get server's public IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
    except:
        public_ip = "Unable to determine"

    # Get client's IP (the one making the request)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    return render_template('index.html',
                         hostname=hostname,
                         local_ip=local_ip,
                         public_ip=public_ip,
                         client_ip=client_ip)

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
