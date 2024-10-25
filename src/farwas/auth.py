import os


def get_github_headers(token: str = None) -> dict:
    if token is None:
        token = os.getenv("GITHUB_TOKEN")
        if token is None:
            raise ValueError(
                "Please provide a GitHub token or set GITHUB_TOKEN environment variable"
            )

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Python/3.12",
    }
