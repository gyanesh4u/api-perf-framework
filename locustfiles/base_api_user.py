from locust import HttpUser, between
import yaml
from auth.jwt import get_jwt_token

class BaseApiUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """
        Initialize user: load config and obtain JWT token.
        """
        try:
            # Load configuration
            with open("config/env.yaml") as f:
                self.config = yaml.safe_load(f)

            self.host = self.config["host"]
            
            # Obtain JWT token
            token = get_jwt_token(self.config)

            # Set authorization headers
            self.client.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        except Exception as e:
            raise Exception(f"Failed to initialize user: {e}")

