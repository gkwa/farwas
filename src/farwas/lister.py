import typing

from .api import GitHubAPI
from .auth import get_github_headers


class GitHubRepoLister:
    def __init__(
        self, token: str = None, cache_dir: str = None, no_cache: bool = False
    ):
        headers = get_github_headers(token)
        self.api = GitHubAPI(headers, cache_dir=cache_dir, no_cache=no_cache)

    def _enrich_with_workflow_status(
        self, repos: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        for repo in repos:
            status = self.api.fetch_latest_workflow_status(repo["name"])
            repo["workflow_status"] = status
        return repos

    def list_user_repos(
        self, username: str, limit: int = 20, view: str = "view1"
    ) -> typing.List[typing.Dict]:
        try:
            url = f"https://api.github.com/users/{username}/repos?sort=pushed&direction=desc&per_page={limit}"
            repos = self.api.fetch_repos(url, limit)
            if view in ["view3", "view4"]:
                repos = self._enrich_with_workflow_status(repos)
            return repos
        except Exception as e:
            raise Exception(f"Error fetching repositories: {str(e)}")

    def list_org_repos(
        self, org: str, limit: int = 20, view: str = "view1"
    ) -> typing.List[typing.Dict]:
        try:
            url = f"https://api.github.com/orgs/{org}/repos?sort=pushed&direction=desc&per_page={limit}"
            repos = self.api.fetch_repos(url, limit)
            if view in ["view3", "view4"]:
                repos = self._enrich_with_workflow_status(repos)
            return repos
        except Exception as e:
            raise Exception(f"Error fetching repositories: {str(e)}")
