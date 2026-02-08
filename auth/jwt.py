import requests

def get_jwt_token(config):
    """
    Obtain JWT token from the configured token endpoint.
    
    Args:
        config: Configuration dictionary containing host, auth details
        
    Returns:
        JWT access token string or empty string if no auth needed
        
    Raises:
        ValueError: If required config keys are missing
        Exception: If token request fails
    """
    # Check if authentication is disabled
    if config.get("auth", {}).get("type") == "none":
        return ""
    
    # Validate required configuration
    required_keys = ["host", "auth"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    auth_config = config["auth"]
    required_auth_keys = ["token_url", "username", "password"]
    for key in required_auth_keys:
        if key not in auth_config:
            raise ValueError(f"Missing required auth config key: {key}")
    
    try:
        url = config["host"] + auth_config["token_url"]
        payload = {
            "username": auth_config["username"],
            "password": auth_config["password"]
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        token = response.json().get("access_token", "")
        
        if not token:
            raise ValueError("No access_token in response")
        
        return token
    except requests.RequestException as e:
        raise Exception(f"Failed to obtain JWT token: {e}")

