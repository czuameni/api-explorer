import requests
import time
import json
from typing import Optional

from app.models.request_model import RequestModel
from app.models.response_model import ResponseModel


class RequestEngine:

    @staticmethod
    def send(request: RequestModel) -> ResponseModel:
        start_time = time.time()

        try:
            response = requests.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                params=request.params,
                json=request.body if isinstance(request.body, dict) else None,
                data=request.body if isinstance(request.body, str) else None,
                auth=RequestEngine._build_auth(request.auth)
            )

            end_time = time.time()

            response_time = round((end_time - start_time) * 1000, 2)  # ms
            size = len(response.content)

            parsed_body = RequestEngine._parse_response_body(response)

            return ResponseModel(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=parsed_body,
                response_time=response_time,
                size=size
            )

        except Exception as e:
            return ResponseModel(
                status_code=0,
                headers={},
                body={"error": str(e)},
                response_time=0,
                size=0
            )

    @staticmethod
    def _parse_response_body(response: requests.Response):
        try:
            return response.json()
        except Exception:
            return response.text

    @staticmethod
    def _build_auth(auth_data: Optional[dict]):
        if not auth_data:
            return None

        if auth_data.get("type") == "basic":
            return (auth_data.get("username"), auth_data.get("password"))

        return None