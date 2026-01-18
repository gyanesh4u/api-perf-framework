from locust import task
from .base_api_user import BaseApiUser
import yaml
import random

class ApiUser(BaseApiUser):

    def on_start(self):
        super().on_start()
        with open("scenarios/users_api.yaml") as f:
            self.scenario = yaml.safe_load(f)

    @task
    def execute(self):
        # Use weighted random selection based on task weights
        weights = [req["weight"] for req in self.scenario["requests"]]
        req = random.choices(self.scenario["requests"], weights=weights, k=1)[0]
        self.client.request(
            method=req["method"],
            url=self.host + req["endpoint"],
            json=req.get("payload"),
            name=req["name"]
        )
