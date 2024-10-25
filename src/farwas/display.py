import typing


def print_repos_view1(repos: typing.List[typing.Dict]) -> None:
    print(f"Showing {len(repos)} repositories")
    print("NAME                        DESCRIPTION  INFO    UPDATED")
    for repo in repos:
        name = repo["name"].ljust(28)
        description = (
            repo["description"][:30] + "..."
            if len(repo["description"]) > 30
            else repo["description"]
        ).ljust(12)
        visibility = repo["visibility"].ljust(8)
        updated = repo["updated"]
        print(f"{name}{description}{visibility}{updated}")


def print_repos_view2(repos: typing.List[typing.Dict]) -> None:
    print(f"Showing {len(repos)} repositories")
    for repo in repos:
        name = repo["name"].ljust(40)
        visibility = repo["visibility"].ljust(8)
        updated = repo["updated"]
        print(f"{name}{visibility}{updated}")
        print(f"https://github.com/{repo['name']}/actions")
        print(f"https://github.com/{repo['name']}/commits")
        print()


def print_repos_view3(repos: typing.List[typing.Dict]) -> None:
    print(f"Showing {len(repos)} repositories")
    for repo in repos:
        name = repo["name"].ljust(40)
        visibility = repo["visibility"].ljust(8)
        updated = repo["updated"]
        status = repo.get("workflow_status", "no workflows")
        print(f"{name}{visibility}{updated}")
        print(f"Actions Status: {status}")
        print(f"https://github.com/{repo['name']}/actions")
        print(f"https://github.com/{repo['name']}/commits")
        print()


def extract_minutes(time_str: str) -> int:
    if "minutes" in time_str:
        return int(time_str.split()[1])
    elif "hours" in time_str:
        return int(time_str.split()[1]) * 60
    elif "days" in time_str:
        return int(time_str.split()[0]) * 24 * 60
    return 0


def print_repos_view4(repos: typing.List[typing.Dict]) -> None:
    print(f"Showing {len(repos)} repositories")

    def status_priority(status):
        if status == "failure":
            return 0
        elif status == "success":
            return 1
        else:
            return 2

    def sort_key(repo):
        status = repo.get("workflow_status")
        return (status_priority(status), extract_minutes(repo["updated"]), repo["name"])

    sorted_repos = sorted(repos, key=sort_key)

    for repo in sorted_repos:
        status = repo.get("workflow_status", "no workflows")
        status = status if status else "no workflows"
        updated = repo["updated"]
        if status == "no workflows":
            url = f"https://github.com/{repo['name']}"
        else:
            url = f"https://github.com/{repo['name']}/actions"
        print(f"{status:<12} {updated:<25} {url}")


def print_repos(repos: typing.List[typing.Dict], view: str = "view1") -> None:
    if view == "view2":
        print_repos_view2(repos)
    elif view == "view3":
        print_repos_view3(repos)
    elif view == "view4":
        print_repos_view4(repos)
    else:
        print_repos_view1(repos)
