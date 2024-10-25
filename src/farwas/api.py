import datetime
import hashlib
import json
import typing
import urllib.request
import zoneinfo

from .cache import DiskCache


class GitHubAPI:
    def __init__(self, headers: dict, cache_dir: str = None, no_cache: bool = False):
        self.headers = headers
        self.cache = None if no_cache else DiskCache(cache_dir)

    def _cache_key(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def fetch_repos(self, url: str, limit: int) -> typing.List[typing.Dict]:
        cache_key = self._cache_key(url)
        if self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return cached_data

        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
            repos_data = json.loads(response.read())

        now = datetime.datetime.now(zoneinfo.ZoneInfo("UTC"))
        result = []

        for repo in repos_data[:limit]:
            updated_at = datetime.datetime.fromisoformat(
                repo["updated_at"].replace("Z", "+00:00")
            )
            diff = now - updated_at

            if diff.days == 0:
                if diff.seconds < 3600:
                    time_ago = f"about {diff.seconds // 60} minutes ago"
                else:
                    time_ago = f"about {diff.seconds // 3600} hours ago"
            else:
                time_ago = f"{diff.days} days ago"

            owner = repo["owner"]["login"]
            repo_info = {
                "name": f"{owner}/{repo['name']}",
                "description": repo["description"] or "",
                "visibility": repo["visibility"],
                "updated": time_ago,
            }
            result.append(repo_info)

        if self.cache:
            self.cache.set(cache_key, result)
        return result

    def fetch_latest_workflow_status(self, repo_full_name: str) -> typing.Optional[str]:
        url = f"https://api.github.com/repos/{repo_full_name}/actions/runs?per_page=1"
        cache_key = self._cache_key(url)
        if self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return cached_data

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())

            if data["total_count"] > 0:
                status = data["workflow_runs"][0]["conclusion"] or "in_progress"
                if self.cache:
                    self.cache.set(cache_key, status)
                return status
            return None
        except Exception:
            return None
