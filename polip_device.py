import requests

from urllib.parse import urlencode
from .util import create_timestamp, create_tag
from .constants import POLIP_DEVICE_INGEST_SERVER_URL_SECURE

class PolipDevice:
    def __init__(
        self,
        url=POLIP_DEVICE_INGEST_SERVER_URL_SECURE,
        value=0,
        skip_tag_check=False,
        serial=None,
        key=None,
        hardware=None,
        firmware=None,
        rollover=None
    ):
        self.url = url
        self.value = value  # Incremented value for next transmission id
        self.skip_tag_check = skip_tag_check  # Set true if key -> tag gen not needed
        self.serial = serial  # Serial identifier unique to this device
        self.key = key  # Revocable key used for tag gen
        self.hardware = hardware  # Hardware version to report to server
        self.firmware = firmware  # Firmware version to report to server
        self.rollover = rollover

    def check_server_status(self):
        try:
            response = requests.get(self.url + "/api/device/v1/health/check")
            if response.status_code != 200:
                raise Exception("Server returned non-200 status code")
        except Exception as error:
            raise Exception("Failed to check server status: " + str(error))

    def get_state(self, state=True, meta=False, sensors=False, rpc=False, manufacturer=False):
        params = {
            "meta": meta,
            "state": state,
            "sensors": sensors,
            "rpc": rpc,
            "manufacturer": manufacturer,
        }

        res = self._request_template(self.url + "/api/device/v1/poll?" + urlencode(params))
        print(res)
        return res

    def push_state(self, state_obj):
        if not isinstance(state_obj, dict) or state_obj is None:
            raise Exception("Invalid parameterization: sensor object must be provided")

        res = self._request_template(self.url + "/api/device/v1/push", {"state": state_obj})
        print(res)
        return res

    def push_notification(self, message):
        self.push_error(message, 0)

    def push_error(self, message, error_code):
        message = str(message)
        error_code = int(error_code)

        res = self._request_template(self.url + "/api/device/v1/error", {"code": error_code, "message": message})
        print(res)
        return res

    def push_sensors(self, sensors_obj):
        if not isinstance(sensors_obj, dict) or sensors_obj is None:
            raise Exception("Invalid parameterization: sensor object must be provided")

        res = self._request_template(self.url + "/api/device/v1/sense", {"sense": sensors_obj})
        return res

    def get_value(self):
        res = self._request_template(self.url + "/api/device/v1/value", skip_value=True, skip_tag=True)
        self.value = res["value"]
        print(res)
        return res

    def push_rpc(self, rpc_obj):
        if rpc_obj.get("uuid") is None:
            raise Exception("Invalid parameterization: RPC must have uuid")
        elif rpc_obj.get("result") is None:
            raise Exception("Invalid parameterization: RPC must have result")

        res = self._request_template(self.url + "/api/device/v1/rpc", {"rpc": rpc_obj})
        print(res)
        return res

    def get_schema(self):
        res = self._request_template(self.url + "/api/device/v1/schema")
        print(res)
        return res

    def get_error_semantic(self, code=None):
        uri = self.url + "/api/v1/device/error/semantic" + ("?code=" + str(code)) if code is not None else ""
        res = self._request_template(uri)
        print(res)
        return res

    def _request_template(self, endpoint, req_obj=None, skip_value=False, skip_tag=False):
        if req_obj is None:
            req_obj = {}

        req_obj["serial"] = self.serial
        req_obj["firmware"] = self.firmware
        req_obj["hardware"] = self.hardware
        req_obj["timestamp"] = create_timestamp()

        if not skip_value:
            req_obj["value"] = self.value

        if not skip_tag:
            req_obj["tag"] = "0"
            if not self.skip_tag_check:
                req_obj["tag"] = create_tag(req_obj, self.key)

        response = requests.post(endpoint, json=req_obj)

        if response.status_code != 200:
            if response.text == "value invalid":
                raise Exception("Value invalid")
            else:
                raise Exception("Server error")

        res_data = response.json()

        if not skip_tag and not self.skip_tag_check:
            old_tag = res_data["tag"]
            res_data["tag"] = "0"
            res_data["tag"] = create_tag(res_data, self.key)
            if old_tag != res_data["tag"]:
                raise Exception("Tag match failed")

        if not skip_value:
            self.value += 1
            if self.rollover is not None and self.value >= self.rollover:
                self.value = 0

        return res_data