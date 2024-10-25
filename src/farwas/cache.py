import json
import pathlib
import time
import typing


class DiskCache:
    def __init__(self, cache_dir: str = None, timeout_minutes: int = 10):
        if cache_dir is None:
            cache_dir = pathlib.Path.home() / ".farwas" / "cache"
        self.cache_dir = pathlib.Path(cache_dir)
        self.timeout_seconds = timeout_minutes * 60
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> pathlib.Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> typing.Optional[typing.Dict]:
        cache_path = self._get_cache_path(key)
        try:
            if cache_path.exists():
                with cache_path.open("r") as f:
                    data = json.load(f)
                if time.time() - data["timestamp"] <= self.timeout_seconds:
                    return data["value"]
                cache_path.unlink()
        except Exception:
            pass
        return None

    def set(self, key: str, value: typing.Any) -> None:
        cache_path = self._get_cache_path(key)
        try:
            with cache_path.open("w") as f:
                json.dump({"timestamp": time.time(), "value": value}, f)
        except Exception:
            pass
