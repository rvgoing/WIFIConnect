from flask import Flask, render_template, request, jsonify
import socket
import requests
import time
from datetime import datetime

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

@app.route('/ping')
def ping_page():
    return render_template('ping.html')

@app.route('/api/ping', methods=['POST'])
def ping_test():
    data = request.get_json()
    target = data.get('target', '').strip()

    if not target:
        return jsonify({'success': False, 'error': 'No target specified'}), 400

    results = []

    # Perform multiple ping attempts (5 by default)
    for i in range(5):
        result = perform_ping(target)
        results.append(result)
        if i < 4:  # Don't sleep after the last ping
            time.sleep(1)

    # Calculate statistics
    successful_pings = [r for r in results if r['success']]

    if successful_pings:
        response_times = [r['response_time'] for r in successful_pings]
        stats = {
            'min': min(response_times),
            'max': max(response_times),
            'avg': sum(response_times) / len(response_times),
            'packet_loss': ((5 - len(successful_pings)) / 5) * 100
        }
    else:
        stats = {
            'min': 0,
            'max': 0,
            'avg': 0,
            'packet_loss': 100
        }

    return jsonify({
        'success': True,
        'target': target,
        'results': results,
        'stats': stats
    })

def perform_ping(target):
    """
    Perform a connectivity test to the target.
    Uses TCP socket connection for testing (not ICMP ping).
    """
    result = {
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'success': False,
        'response_time': 0,
        'message': ''
    }

    # Try to resolve hostname if it's not an IP
    try:
        ip_address = socket.gethostbyname(target)
        result['ip'] = ip_address
    except socket.gaierror:
        result['message'] = f'Failed to resolve hostname: {target}'
        return result

    # Try TCP connection on common ports (80 for HTTP, 443 for HTTPS)
    ports_to_try = [80, 443]

    for port in ports_to_try:
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip_address, port))
            end_time = time.time()
            sock.close()

            result['success'] = True
            result['response_time'] = round((end_time - start_time) * 1000, 2)  # Convert to ms
            result['message'] = f'Connection successful to {ip_address}:{port}'
            return result
        except (socket.timeout, socket.error):
            continue

    # If all ports failed, try just checking if host is reachable via HTTP
    try:
        start_time = time.time()
        response = requests.get(f'http://{target}', timeout=3)
        end_time = time.time()

        result['success'] = True
        result['response_time'] = round((end_time - start_time) * 1000, 2)
        result['message'] = f'HTTP connection successful (status: {response.status_code})'
        return result
    except:
        result['message'] = f'Unable to connect to {ip_address}'
        return result

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
