import unittest.mock

import farwas.api


def test_cache_key():
    api = farwas.api.GitHubAPI({})
    key = api._cache_key("https://api.github.com/users/test/repos")
    assert isinstance(key, str)
    assert len(key) == 64


@unittest.mock.patch("urllib.request.urlopen")
def test_fetch_repos_limit(mock_urlopen):
    # Mock the context manager
    cm = unittest.mock.MagicMock()
    cm.read.return_value = b"""[
        {"name": "repo1", "owner": {"login": "test"}, "description": "test repo", 
         "visibility": "public", "updated_at": "2024-03-25T00:00:00Z"},
        {"name": "repo2", "owner": {"login": "test"}, "description": "test repo 2", 
         "visibility": "public", "updated_at": "2024-03-25T00:00:00Z"}
    ]"""
    mock_urlopen.return_value.__enter__.return_value = cm

    api = farwas.api.GitHubAPI({"Authorization": "Bearer test"})
    url = "https://api.github.com/users/test/repos"
    repos = api.fetch_repos(url, limit=1)
    assert isinstance(repos, list)
    assert len(repos) == 1


@unittest.mock.patch("urllib.request.urlopen")
def test_fetch_workflow_status(mock_urlopen):
    # Mock the context manager
    cm = unittest.mock.MagicMock()
    cm.read.return_value = (
        b"""{"total_count": 1, "workflow_runs": [{"conclusion": "success"}]}"""
    )
    mock_urlopen.return_value.__enter__.return_value = cm

    api = farwas.api.GitHubAPI({"Authorization": "Bearer test"})
    status = api.fetch_latest_workflow_status("test/repo")
    assert status == "success"
