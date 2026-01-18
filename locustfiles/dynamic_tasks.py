from locust import task
from base_api_user import BaseApiUser
import yaml
import random

class ApiUser(BaseApiUser):

    def on_start(self):
        super().on_start()
        with open("scenarios/users_api.yaml") as f:
            self.scenario = yaml.safe_load(f)

    @task
    def execute(self):
        req = random.choice(self.scenario["requests"])
        self.client.request(
            method=req["method"],
            url=req["endpoint"],
            json=req.get("payload"),
            name=req["name"]
        )
