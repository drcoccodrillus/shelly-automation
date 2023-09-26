# -*- coding: utf-8 -*-

import requests
import json
import re

from datetime import datetime

# Shelly Button1 API
# https://shelly-api-docs.shelly.cloud/#shelly-button1

DEFAULT_IP_ADDRESS = "192.168.33.1"
IP_ADDRESS = "192.168.10.100"

BASE_URL = "http://"
END_POINTS = {
    "status": "/status",
    "base": "/settings",
    "access-point": "/settings/ap",
    "wifi": "/settings/sta",
    "actions": "/settings/actions"
}

class ShellyButton1:
    def __init__(self, url1=None, url2=None, url3=None, url4=None):
        self.url1 = url1
        self.url2 = url2
        self.url3 = url3
        self.url4 = url4

    def create_url(self, endpoint, kickoff=False, ip_address=None, params=None):
        if kickoff:
            url = f'{BASE_URL}{DEFAULT_IP_ADDRESS}{endpoint}'
        elif ip_address:
            pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            if pattern.match(ip_address):
                url = f'{BASE_URL}{ip_address}{endpoint}'
            else:
                url = f'{BASE_URL}{DEFAULT_IP_ADDRESS}{endpoint}'
        else:
            url = f'{BASE_URL}{IP_ADDRESS}{endpoint}'

        if params:
            param_string = "&".join([f"{key}={value}" for key, value in params.items()])
            url = f"{url}?{param_string}"

        return url

    def status(self, kickoff=False, ip_address=None):
        try:
            response = requests.get(self.create_url(END_POINTS["status"], kickoff, ip_address))
        except Exception as e:
            print('status API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_device_name(self, device_name, kickoff=False, ip_address=None):
        try:
            raw_data = f"name={device_name}"
            response = requests.post(self.create_url(END_POINTS["base"], kickoff, ip_address), data=raw_data)
        except Exception as e:
            print('set_device_name API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_wifi_access_point_mode(self, key, kickoff=False, ip_address=None):
        params = {
            "enabled": "1",
            "key": key
        }
        try:
            response = requests.get(self.create_url(END_POINTS["access-point"], kickoff, ip_address, params=params))
        except Exception as e:
            print("enable_acess_point_mode API error:", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "message": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_wifi_client_mode(self, ssid, key, ipv4_method, ip, netmask, gateway, dns, kickoff=False, ip_address=None):
        params = {
            "enabled": "1",
            "ssid": ssid,
            "key": key,
            "ipv4_method": ipv4_method,
            "ip": ip,
            "netmask": netmask,
            "gateway": gateway,
            "dns": dns
        }
        try:
            response = requests.get(self.create_url(END_POINTS["wifi"], kickoff, ip_address, params=params))
        except Exception as e:
            print("set_wifi_client_mode API error:", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "message": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_timezone(self):
        params = {
            "tzautodetect": "false",
            "timezone": "UTC",
            "tz_utc_offset": "0",
            "lat": "500",
            "lng": "500",
            "tz_dst_auto": "1"
        }
        try:
            response = requests.get(self.create_url_first_setup(END_POINTS["base"], params=params))
        except Exception as e:
            print('disable_timezone API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            print("disable_timezone result:")
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def enable_timezone(self):
        params = {
            "tzautodetect": "true"
        }
        try:
            response = requests.get(self.create_url(END_POINTS["base"], params=params))
        except Exception as e:
            print('enable_timezone API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_led_status(self):
        try:
            params = {
                "led_status_disable": "true"
            }
            response = requests.post(END_POINTS["base"], params=params)
        except Exception as e:
            print('disable_led_status API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def enable_led_status(self):
        try:
            params = {
                "led_status_disable": "false"
            }
            response = requests.post(END_POINTS["base"], params=params)
        except Exception as e:
            print('enable_led_status API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_longpush_duration(self, longpush_duration_ms_max):
        try:
            payload = {"longpush_duration_ms_max": longpush_duration_ms_max}
            response = requests.post(END_POINTS["base"], json=payload)
        except Exception as e:
            print('set_long_push_duration API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def enable_longpush_url(self):
        #http://192.168.10.100/settings/actions/?index=0&enabled=true&name=longpush_url
        try:
            params = {
                "index": "0",
                "enabled": "true",
                "name": "longpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], params=params))
        except Exception as e:
            print('enable_longpush_url API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_longpush_url(self):
        #http://192.168.10.100/settings/actions/?index=0&enabled=false&name=longpush_url
        try:
            params = {
                "index": "0",
                "enabled": "false",
                "name": "longpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], params=params))
        except Exception as e:
            print('disable_longpush_url API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False
