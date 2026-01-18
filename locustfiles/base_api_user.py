from locust import HttpUser, between
import yaml
from auth.jwt import get_jwt_token

class BaseApiUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        with open("config/env.yaml") as f:
            self.config = yaml.safe_load(f)

        self.host = self.config["host"]
        token = get_jwt_token(self.config)

        self.client.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
