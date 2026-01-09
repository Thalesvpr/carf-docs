# GEOGIS + Keycloak (Python/QGIS)

## Install
```bash
pip install requests python-keycloak
```

## Config
```python
# keycloak_config.py
KEYCLOAK_URL = "http://localhost:8080"
REALM = "carf"
CLIENT_ID = "geogis"
CLIENT_SECRET = "your-client-secret"
```

## Auth Client
```python
# auth_client.py
import requests
from datetime import datetime, timedelta

class KeycloakAuth:
    def __init__(self):
        self.token = None
        self.refresh_token = None
        self.expires_at = None

    def login(self, client_id, client_secret):
        """Client Credentials flow"""
        url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

        result = response.json()
        self.token = result['access_token']
        self.expires_at = datetime.now() + timedelta(seconds=result['expires_in'])

    def get_token(self):
        """Get valid token (refresh if needed)"""
        if not self.token or datetime.now() >= self.expires_at:
            self.login(CLIENT_ID, CLIENT_SECRET)
        return self.token

    def request(self, method, url, **kwargs):
        """Make authenticated request"""
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self.get_token()}'
        return requests.request(method, url, headers=headers, **kwargs)
```

## Usage in QGIS Plugin
```python
# plugin.py
from .auth_client import KeycloakAuth

class CarfGeoGISPlugin:
    def __init__(self, iface):
        self.auth = KeycloakAuth()
        self.auth.login(CLIENT_ID, CLIENT_SECRET)

    def fetch_units(self):
        """Fetch units from API"""
        response = self.auth.request('GET', f'{API_URL}/units')
        return response.json()

    def upload_geometry(self, unit_id, geometry):
        """Upload validated geometry"""
        data = {'geometry': geometry}
        response = self.auth.request('PUT', f'{API_URL}/units/{unit_id}', json=data)
        return response.status_code == 200
```

## Token Refresh
```python
def refresh_token(self, refresh_token):
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=data)
    result = response.json()
    self.token = result['access_token']
    self.refresh_token = result['refresh_token']
```

Done. ✅
