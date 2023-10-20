from flask import Flask, request, jsonify
import json
from ShellyButton1 import ShellyButton1

app = Flask(__name__)
shelly = ShellyButton1()

@app.route('/get-status', methods=['GET'])
def status():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.status(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to get status"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-device-name', methods=['POST'])
def set_device_name():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        device_name = data.get('device_name')

        result = shelly.set_device_name(device_name, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Device name is now set", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set device name"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-wifi-access-point-mode', methods=['POST'])
def set_wifi_access_point_mode():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        key = data.get('key')

        result = shelly.set_wifi_access_point_mode(key, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Access point mode is now on", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to enable access point mode"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-wifi-client-mode', methods=['POST'])
def set_wifi_client_mode():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        ssid = data.get('ssid')
        key = data.get('key')
        ipv4_method = data.get('ipv4_method')
        ip = data.get('ip')
        netmask = data.get('netmask')
        gateway = data.get('gateway')
        dns = data.get('dns')

        result = shelly.set_wifi_client_mode(ssid, key, ipv4_method, ip, netmask, gateway, dns, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "WiFi client mode is now on", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set WiFi client mode"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-custom-timezone', methods=['POST'])
def set_custom_timezone():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        timezone = data.get('timezone')
        utc_offset = data.get('utc_offset')

        result = shelly.set_custom_timezone(timezone, utc_offset, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Custom timezone is now set", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set custom timezone"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-automatic-timezone', methods=['POST'])
def set_automatic_timezone():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.set_automatic_timezone(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Automatic timezone is now set", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set automatic timezone"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/disable-led-status', methods=['POST'])
def disable_led_status():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.disable_led_status(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "LED status is now disabled", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to disable LED status"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/enable-led-status', methods=['POST'])
def enable_led_status():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.enable_led_status(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "LED status is now enabled", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to enable LED status"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-longpush-duration', methods=['POST'])
def set_longpush_duration():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        longpush_duration_ms_max = data.get('longpush_duration_ms_max')

        result = shelly.set_longpush_duration(longpush_duration_ms_max, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Longpush duration is now set", "shelly-response": json.loads(result)}), 200

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/enable-longpush', methods=['POST'])
def enable_longpush():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.enable_longpush(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Longpush is now enabled", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to enable longpush"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/disable-longpush', methods=['POST'])
def disable_longpush():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        result = shelly.disable_longpush(kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Longpush is now disabled", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to disable longpush"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

@app.route('/set-longpush-url', methods=['POST'])
def set_longpush_url():
    try:
        kickoff = request.args.get('kickoff', False)
        ip_address = request.args.get('ip_address', None)

        data = request.json

        urls = data.get('urls')

        result = shelly.set_longpush_url(urls, kickoff, ip_address)

        if result:
            return jsonify({"status": "OK", "message": "Longpush URL is now set", "shelly-response": json.loads(result)}), 200

        return jsonify({"error": True, "message": "Failed to set longpush URL"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5080)
