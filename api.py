import time
import requests
from collections import OrderedDict

BASE_URL = 'https://api.curseforge.com'
CACHE_TTL = 10 * 60 # 10 minutes

class Api:
    def __init__(self, api_key: str, cache_max_size=100) -> None:
        self.api_key = api_key
        self.headers = {"x-api-key": api_key}

        self._ttl = CACHE_TTL
        self._max_cache_size = cache_max_size

        # OrderedDict for predictable eviction (FIFO)
        self._version_cache = OrderedDict()  # mod_id -> (timestamp, (versions, loaders))
        self._name_cache = OrderedDict()     # mod_id -> (timestamp, name)

    def _get(self, endpoint: str, params=None):
        """Helper for GET requests with consistent headers and error handling."""
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching {url}: HTTP {response.status_code}")
            return None
        return response.json()

    def _set_cache(self, cache: OrderedDict, key, value):
        """Insert value into cache with eviction policy."""
        cache[key] = (time.time(), value)
        cache.move_to_end(key)
        if len(cache) > self._max_cache_size:
            cache.popitem(last=False)  # Evict oldest entry (FIFO)

    def _get_cached(self, cache: OrderedDict, key):
        """Return cached value if valid, otherwise None."""
        if key in cache:
            cached_time, value = cache[key]
            if time.time() - cached_time < self._ttl:
                return value
            else:
                del cache[key]
        return None

    def get_mod_versions_and_loaders(self, mod_id):
        """Get all Minecraft versions and loaders for all files of a mod (with pagination)."""
        cached = self._get_cached(self._version_cache, mod_id)
        if cached:
            return cached

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
            time.sleep(0.2)  # Polite pause to avoid rate limits

        mc_versions = sorted(v for v in versions if v.startswith("1."))
        result = (mc_versions, loaders)

        self._set_cache(self._version_cache, mod_id, result)
        return result

    def get_mod_name(self, mod_id):
        """Fetch the mod name given its ID."""
        cached = self._get_cached(self._name_cache, mod_id)
        if cached:
            return cached

        data = self._get(f"/v1/mods/{mod_id}")
        if not data:
            return None

        name = data.get("data", {}).get("name")
        self._set_cache(self._name_cache, mod_id, name)
        return name

