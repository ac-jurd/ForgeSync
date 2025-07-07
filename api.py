import time
import requests

BASE_URL = 'https://api.curseforge.com'

class Api:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.headers = {"x-api-key": api_key}

    def _get(self, endpoint: str, params=None):
        """Helper for GET requests with consistent headers and error handling."""
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching {url}: HTTP {response.status_code}")
            return None
        return response.json()

    def get_mod_versions_and_loaders(self, mod_id):
        """Get all Minecraft versions and loaders for all files of a mod (with pagination)."""
        versions = set()
        loaders = set()
        page_size = 50
        index = 0

        while True:
            params = {"pageSize": page_size, "index": index}
            data = self._get(f"/v1/mods/{mod_id}/files", params)
            if not data or not data.get("data"):
                break

            for file in data["data"]:
                versions.update(file.get("gameVersions", []))
                loaders.update(file.get("loaders", []))

            index += page_size
            time.sleep(0.2)  # polite pause

        mc_versions = sorted(v for v in versions if v.startswith("1."))  # filter MC versions
        return mc_versions, loaders

    def get_mod_name(self, mod_id):
        """Fetch the mod name given its ID."""
        data = self._get(f"/v1/mods/{mod_id}")
        if not data:
            return None
        return data.get("data", {}).get("name")

