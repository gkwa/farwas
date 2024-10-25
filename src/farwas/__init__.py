from .cli import parse_args
from .display import print_repos
from .lister import GitHubRepoLister


def main() -> None:
    args = parse_args()
    lister = GitHubRepoLister(cache_dir=args.cache_dir, no_cache=args.no_cache)

    if args.user:
        repos = lister.list_user_repos(args.user, args.limit, args.view)
    else:
        repos = lister.list_org_repos(args.org, args.limit, args.view)

    print_repos(repos, args.view)
