# -*- coding: utf-8 -*-

import subprocess
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
            param_string = "&".join([f"{key}={value}" for key, value in params.items() if key != "urls"])
            urls = "&".join([f"urls[]={url}" for url in params["urls"] if len(params["urls"]) > 0 and len(params["urls"]) < 6 and isinstance(params["urls"], list)]) if "urls" in params else ""
            param_string = f"{param_string}&{urls}" if urls else param_string
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

    def set_custom_timezone(self, timezone, utc_offset, kickoff=False, ip_address=None):
        params = {
            "tzautodetect": "false",
            "timezone": timezone,
            "tz_utc_offset": utc_offset,
            "lat": "500",
            "lng": "500",
            "tz_dst_auto": "1"
        }
        try:
            response = requests.get(self.create_url(END_POINTS["base"], kickoff, ip_address, params=params))
        except Exception as e:
            print('set_custom_timezone API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            print("set_custom_timezone result:")
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_automatic_timezone(self, kickoff=False, ip_address=None):
        params = {
            "tzautodetect": "true"
        }
        try:
            response = requests.get(self.create_url(END_POINTS["base"], kickoff, ip_address, params=params))
        except Exception as e:
            print('enable_timezone API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_led_status(self, kickoff=False, ip_address=None):
        try:
            params = {
                "led_status_disable": "true"
            }
            response = requests.post(self.create_url(END_POINTS["base"], kickoff, ip_address, params=params))
        except Exception as e:
            print('disable_led_status API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def enable_led_status(self, kickoff=False, ip_address=None):
        try:
            params = {
                "led_status_disable": "false"
            }
            response = requests.post(self.create_url(END_POINTS["base"], kickoff, ip_address, params=params))
        except Exception as e:
            print('enable_led_status API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_longpush_duration(self, longpush_duration_ms_max, kickoff=False, ip_address=None):
        try:
            raw_data = f"longpush_duration_ms_max={longpush_duration_ms_max}"
            response = requests.post(self.create_url(END_POINTS["base"], kickoff, ip_address), data=raw_data)
        except Exception as e:
            print('set_long_push_duration API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_multipush(self, multipush_ms_max, kickoff=False, ip_address=None):
        try:
            raw_data = f"multipush_time_between_pushes_ms_max={multipush_ms_max}"
            response = requests.post(self.create_url(END_POINTS["base"], kickoff, ip_address), data=raw_data)
        except Exception as e:
            print('set_multipush API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def enable_longpush(self, kickoff=False, ip_address=None):
        #http://192.168.10.100/settings/actions/?index=0&enabled=true&name=longpush_url
        try:
            params = {
                "index": "0",
                "enabled": "true",
                "name": "longpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params))
        except Exception as e:
            print('enable_longpush_url API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_longpush(self, kickoff=False, ip_address=None):
        #http://192.168.10.100/settings/actions/?index=0&enabled=false&name=longpush_url
        try:
            params = {
                "index": "0",
                "enabled": "false",
                "name": "longpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params))
        except Exception as e:
            print('disable_longpush_url API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_longpush_url(self, urls, kickoff=False, ip_address=None):
        #http://192.168.10.100/settings/actions/?index=0&enabled=true&name=longpush_url&urls[]=http://localhost/target1&urls[]=http://localhost/target2
        # This API uses curl instead of requests because the requests library does not handle the "urls[]" parameter as expected by the Shelly API
        # The requests library encodes the "urls[]" parameter as "urls%5B%5D" which is not accepted by the Shelly API
        try:
            params = {
                "index": "0",
                "enabled": "true",
                "name": "longpush_url",
                "urls": urls
            }
            curl_command = ["curl", "-s", "-w", "%{http_code}", self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params)]
            response = subprocess.check_output(curl_command, stderr=subprocess.STDOUT, text=True)
            response_body = response[:-3]       # Extract the response body
            response_code = int(response[-3:])  # Extract the HTTP status code
            print(response[-3:])
        except subprocess.CalledProcessError as e:
            print(f"Request failed with error: {e.returncode}")
            print(e.output)

        if response_code == 200:
            json_object = json.loads(response_body)
            return json.dumps(json_object, indent=2)

        return False

    def enable_shortpush(self, kickoff=False, ip_address=None):
        #http://192.168.10.100/settings/actions/?index=0&enabled=true&name=shortpush_url
        try:
            params = {
                "index": "0",
                "enabled": "true",
                "name": "shortpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params))
        except Exception as e:
            print('enable_shortpush API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def disable_shortpush(self, kickoff=False, ip_address=None):
        #http://192.168.10.100/settings/actions/?index=0&enabled=false&name=shortpush_url
        try:
            params = {
                "index": "0",
                "enabled": "false",
                "name": "shortpush_url"
            }
            response = requests.get(self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params))
        except Exception as e:
            print('disable_shortpush API error:', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            return {"error": True, "exception": e}

        if response.status_code == 200:
            json_object = json.loads(response.text)
            return json.dumps(json_object, indent=2)

        return False

    def set_shortpush_url(self, urls, kickoff=False, ip_address=None):
        #http://192.168.10.187/settings/actions/?index=0&enabled=true&name=shortpush_url&urls[]=http://localhost/target1&urls[]=http://localhost/target2
        # This API uses curl instead of requests because the requests library does not handle the "urls[]" parameter as expected by the Shelly API
        # The requests library encodes the "urls[]" parameter as "urls%5B%5D" which is not accepted by the Shelly API
        try:
            params = {
                "index": "0",
                "enabled": "true",
                "name": "shortpush_url",
                "urls": urls
            }
            curl_command = ["curl", "-s", "-w", "%{http_code}", self.create_url(END_POINTS["actions"], kickoff, ip_address, params=params)]
            response = subprocess.check_output(curl_command, stderr=subprocess.STDOUT, text=True)
            response_body = response[:-3]       # Extract the response body
            response_code = int(response[-3:])  # Extract the HTTP status code
            print(response[-3:])
        except subprocess.CalledProcessError as e:
            print(f"Request failed with error: {e.returncode}")
            print(e.output)

        if response_code == 200:
            json_object = json.loads(response_body)
            return json.dumps(json_object, indent=2)

        return False