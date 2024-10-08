import requests
from urllib.parse import urlencode
from flask import request
from scheduler.log import logger
from scheduler.config import Config


class CoreApi:
    def __init__(self):
        self.api_url = Config.TARANIS_CORE_URL
        self.jwt_token = self.get_jwt_from_request()
        self.headers = self.get_headers()
        self.verify = Config.SSL_VERIFICATION
        self.timeout = Config.REQUESTS_TIMEOUT

    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.jwt_token}", "Content-type": "application/json"}

    def get_jwt_from_request(self):
        return request.cookies.get(Config.JWT_ACCESS_COOKIE_NAME)

    def check_response(self, response: requests.Response, url: str):
        try:
            if response.ok:
                return response.json()
        except Exception:
            logger.error(f"Call to {url} failed {response.status_code}: {response.text}")
        logger.error(f"Call to {url} failed {response.status_code}: {response.text}")
        return None

    def api_put(self, url, json_data=None):
        url = f"{self.api_url}{url}"
        if not json_data:
            json_data = {}
        response = requests.put(url=url, headers=self.headers, verify=self.verify, json=json_data, timeout=self.timeout)
        return self.check_response(response, url)

    def api_post(self, url, json_data=None):
        url = f"{self.api_url}{url}"
        if not json_data:
            json_data = {}
        response = requests.post(url=url, headers=self.headers, verify=self.verify, json=json_data, timeout=self.timeout)
        return self.check_response(response, url)

    def api_get(self, url, params=None):
        url = f"{self.api_url}{url}"
        if params:
            url += f"?{urlencode(params)}"
        try:
            response = requests.get(url=url, headers=self.headers, verify=self.verify, timeout=self.timeout)
        except Exception as e:
            logger.error(f"Call to {url} failed {e}")
            return None
        return self.check_response(response, url)

    def api_delete(self, url):
        url = f"{self.api_url}{url}"
        response = requests.delete(url=url, headers=self.headers, verify=self.verify, timeout=self.timeout)
        return self.check_response(response, url)

    def get_schedule(self, query_params=None):
        return self.api_get("/config/schedule", params=query_params)

    def get_schedule_by_id(self, schedule_id):
        return self.api_get(f"/config/schedule/{schedule_id}")

    def add_schedule(self, schedule_data):
        return self.api_post("/config/schedule", json_data=schedule_data)

    def update_schedule(self, schedule_id, schedule_data):
        return self.api_put(f"/config/schedule/{schedule_id}", json_data=schedule_data)

    def delete_schedule(self, schedule_id):
        return self.api_delete(f"/config/schedule/{schedule_id}")
