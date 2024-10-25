import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List GitHub repositories")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user", "-u", help="GitHub username")
    group.add_argument("--org", "-o", help="GitHub organization")
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=20,
        help="Number of repositories to display (default: 20)",
    )
    parser.add_argument(
        "--cache-dir",
        help="Directory to store cache files (default: ~/.farwas/cache)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching of API requests",
    )
    parser.add_argument(
        "view",
        nargs="?",
        choices=["view1", "view2", "view3", "view4"],
        default="view1",
        help="Display format (default: view1)",
    )
    return parser.parse_args()
