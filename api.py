from flask import Flask, request, jsonify
import json
from ShellyButton1 import ShellyButton1

app = Flask(__name__)
shelly = ShellyButton1()

@app.route('/set-wifi-client-mode', methods=['POST'])
def set_wifi_client_mode():
    try:
        data = request.json

        ssid = data.get('ssid')
        key = data.get('key')
        ipv4_method = data.get('ipv4_method')
        ip = data.get('ip')
        netmask = data.get('netmask')
        gateway = data.get('gateway')
        dns = data.get('dns')
        kickoff = data.get('kickoff', False)

        result = shelly.set_wifi_client_mode(ssid, key, ipv4_method, ip, netmask, gateway, dns, kickoff)

        if result:
            return jsonify({"status": "OK", "message": "WiFi client mode is now on", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set WiFi client mode"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5080)
