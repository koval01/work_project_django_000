from datetime import datetime

from requests import request
import os


class KeitaroBase:
    def __init__(self) -> None:
        self.host: str = os.getenv("KEITARO_HOST")
        self.token: str = os.getenv("KEITARO_TOKEN")

    def _request_body(self, path: str, json: dict) -> dict:
        return {
            "url": f"{self.host}/admin_api/v1/{path}",
            "headers": {"Api-Key": self.token},
            "json": json
        }

    def request(self, method: str, path: str, json: dict) -> request or None:
        response = request(method, **self._request_body(path, json))
        return response if response.status_code >= 200 < 300 else None


class Keitaro:
    def __init__(self) -> None:
        self.ApiClass = KeitaroBase()

    def report(self, from_: datetime, to: datetime, grouping: list = None, metrics: list = None) -> dict:
        return self.ApiClass.request(
            method="POST", path="report/build",
            json={
                "range": {
                    "from": from_.strftime("%Y-%m-%d"),
                    "to": to.strftime("%Y-%m-%d"),
                    "timezone": "Europe/Kiev"
                },
                "grouping": grouping,
                "metrics": metrics
            }
        ).json()
