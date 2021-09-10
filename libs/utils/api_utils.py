import json
from poium.common import logging
import time
from libs.common.request import ApiRequest
from libs.utils.misc import Misc


class InterfaceType:
    SensorData = 1
    AlertData = 2
    LEDLuminosity = 3
    RadarData = 4


class APIUtils:

    def __init__(self):
        self.config = Misc.load_config()
        self.host = self.config["api_host"]

    def get_user_token(self, secret_key, is_return=True):
        """
        Obtain token by user secret keys in order to complete API authentication
        """
        response = ApiRequest\
            .get(self.host)\
            .add_path("pxp/iot/Device/jwtGenerate.json")\
            .add_param("info", secret_key)\
            .is_verify(False) \
            .send()

        return response if not is_return else response.json()["result"]["idToken"]

    def sensor_data(self, id_token, device_id, start_time, end_time, data_type="peopleCnt",
                    interface_type=InterfaceType.SensorData, page_number=1, page_size=100, is_304=False):
        """
        Get information of a period of a device
        """
        if is_304:
            response = ApiRequest \
                .get(self.host) \
                .add_path("pxp/iot/Device/findDeviceData.json") \
                .add_param("deviceId", device_id) \
                .add_param("interfaceType", interface_type) \
                .add_param("dataType", data_type) \
                .add_param("startTime", start_time) \
                .add_param("endTime", end_time) \
                .add_param("pageNo", page_number) \
                .add_param("page_size", page_size) \
                .add_header("idToken", id_token)\
                .is_verify(False) \
                .send()
            return response
        else:
            status = 304
            while status == 304:
                response = ApiRequest \
                    .get(self.host) \
                    .add_path("pxp/iot/Device/findDeviceData.json") \
                    .add_param("deviceId", device_id) \
                    .add_param("interfaceType", interface_type) \
                    .add_param("dataType", data_type) \
                    .add_param("startTime", start_time) \
                    .add_param("endTime", end_time) \
                    .add_param("pageNo", page_number) \
                    .add_param("page_size", page_size) \
                    .add_header("idToken", id_token) \
                    .is_verify(False) \
                    .send()
                if "999999" not in response.text:
                    status = json.loads(response.text)["code"]
                else:
                    status = "999999"
                if status == 304:
                    time.sleep(self.config["jenkins_params"]["interval_min"])
                else:
                    return response

    def alert_data(self, id_token, device_id, interface_type=InterfaceType.AlertData, is_304=False):
        """
        Get device alert history data
        """
        if is_304:
            response = ApiRequest \
                .get(self.host) \
                .add_path("pxp/iot/Device/findDeviceData.json") \
                .add_param("deviceId", device_id) \
                .add_param("interfaceType", interface_type) \
                .add_header("idToken", id_token) \
                .is_verify(False) \
                .send()
            return response
        else:
            status = 304
            while status == 304:
                response = ApiRequest \
                    .get(self.host) \
                    .add_path("pxp/iot/Device/findDeviceData.json") \
                    .add_param("deviceId", device_id) \
                    .add_param("interfaceType", interface_type) \
                    .add_header("idToken", id_token)\
                    .is_verify(False) \
                    .send()
                status = json.loads(response.text)["code"]
                if status == 304:
                    logging.info(status)
                    time.sleep(self.config["jenkins_params"]["interval_min"])
                else:
                    return response

    def radar_data(self, id_token, device_id, interface_type=InterfaceType.RadarData, is_304=False, **kwargs):
        """
        Send radar changing requests to devices
        """
        if is_304:
            request = ApiRequest \
                .get(self.host) \
                .add_path("pxp/iot/Device/findDeviceData.json") \
                .add_param("deviceId", device_id) \
                .add_param("interfaceType", interface_type)

            for item in kwargs.items():
                request.add_param(item[0], item[1])

            response = request\
                .add_header("idToken", id_token)\
                .is_verify(False) \
                .send()
            return response
        else:
            status = 304
            while status == 304:
                request = ApiRequest \
                    .get(self.host) \
                    .add_path("pxp/iot/Device/findDeviceData.json") \
                    .add_param("deviceId", device_id) \
                    .add_param("interfaceType", interface_type)

                for item in kwargs.items():
                    request.add_param(item[0], item[1])

                response = request \
                    .add_header("idToken", id_token) \
                    .is_verify(False) \
                    .send()
                status = json.loads(response.text)["code"]
                if status == 304:
                    logging.info(status)
                    time.sleep(self.config["jenkins_params"]["interval_min"])
                else:
                    return response

    def adjust_led_luminosity(self, id_token, device_id, dimming, interface_type=InterfaceType.LEDLuminosity, is_304=False):
        """
        Adjust the LED luminosity of a device
        """
        if is_304:
            response = ApiRequest \
                .get(self.host) \
                .add_path("pxp/iot/Device/findDeviceData.json") \
                .add_param("deviceId", device_id) \
                .add_param("interfaceType", interface_type) \
                .add_param("dimming", dimming) \
                .add_header("idToken", id_token)\
                .set_token(id_token) \
                .is_verify(False) \
                .send()
            return response
        else:
            status = 304
            while status == 304:
                response = ApiRequest \
                    .get(self.host) \
                    .add_path("pxp/iot/Device/findDeviceData.json") \
                    .add_param("deviceId", device_id) \
                    .add_param("interfaceType", interface_type) \
                    .add_param("dimming", dimming) \
                    .add_header("idToken", id_token) \
                    .set_token(id_token) \
                    .is_verify(False) \
                    .send()
                status = json.loads(response.text)["code"]
                if status == 304:
                    logging.info(status)
                    time.sleep(self.config["jenkins_params"]["interval_min"])
                else:
                    return response



