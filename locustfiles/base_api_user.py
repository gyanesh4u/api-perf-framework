from locust import HttpUser, between
import yaml
from auth.jwt import get_jwt_token

class BaseApiUser(HttpUser):
    abstract = True
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
            
            # Obtain JWT token (if auth is enabled)
            token = get_jwt_token(self.config)

            # Set authorization headers
            headers = {"Content-Type": "application/json"}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            self.client.headers.update(headers)
        except Exception as e:
            raise Exception(f"Failed to initialize user: {e}")

