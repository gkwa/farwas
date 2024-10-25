import json
import os
import pathlib
import time
import typing


class DiskCache:
    def __init__(self, cache_dir: str = None, timeout_minutes: int = 10):
        if cache_dir is None:
            cache_dir = os.path.join(str(pathlib.Path.home()), ".farwas", "cache")
        self.cache_dir = cache_dir
        self.timeout_seconds = timeout_minutes * 60
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, key: str) -> typing.Optional[typing.Dict]:
        cache_path = self._get_cache_path(key)
        try:
            if os.path.exists(cache_path):
                with open(cache_path, "r") as f:
                    data = json.load(f)
                if time.time() - data["timestamp"] <= self.timeout_seconds:
                    return data["value"]
                os.remove(cache_path)
        except Exception:
            pass
        return None

    def set(self, key: str, value: typing.Any) -> None:
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, "w") as f:
                json.dump({"timestamp": time.time(), "value": value}, f)
        except Exception:
            pass
