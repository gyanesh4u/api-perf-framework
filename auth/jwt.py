import requests

def get_jwt_token(config):
    url = config["host"] + config["auth"]["token_url"]
    payload = {
        "username": config["auth"]["username"],
        "password": config["auth"]["password"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("access_token", "")
