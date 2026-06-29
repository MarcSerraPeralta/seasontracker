import os
import sys
import argparse
from dotenv import load_dotenv

from .utils import (
    check_tmdb_token,
    check_gmail_app_password,
    check_email,
)
from .gmail import send_email
from .seasons import get_status


def main():
    parser = argparse.ArgumentParser(prog="seasontracker")
    _ = parser.add_argument(
        "yaml_seasons",
        help="YAML file with the seasons information.",
        default=None,
        nargs="?",  # makes positional argument optional
    )

    _ = parser.add_argument(
        "--env",
        help=".env file with (at least) the TMDB API Read Access token (TMDB_TOKEN)",
        default="/home/.seasontracker",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.env):
        print(f"Error: .env file '{args.env}' does not exist.")
        print("Use --env to specify an existing .env file.")
        sys.exit(1)

    _ = load_dotenv(args.env)

    tmdb_token = os.getenv("TMDB_TOKEN")
    if tmdb_token is None:
        print(
            f"Error: 'TMDB_TOKEN' needs to be specified inside .env file '{args.env}'."
        )
        sys.exit(1)
    check_tmdb_token(tmdb_token)

    gmail_account = os.getenv("GMAIL_ACCOUNT")
    if gmail_account is not None:
        check_email(gmail_account)
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    if gmail_app_password is not None:
        check_gmail_app_password(gmail_app_password)

    status = [("test", gmail_account, "test from seasontracker")]
    if args.yaml_seasons is not None:
        if not os.path.isfile(args.yaml_seasons):
            print(f"Error: '{args.yaml_seasons}' does not exist.")
            sys.exit(1)
        status = get_status(args.yaml_seasons, tmdb_token)

    for user, email, text in status:
        if email is None:
            print(f"USER: {user}")
            print(text)
            print("")
            continue

        if gmail_account is None:
            print(
                f"Error: 'GMAIL_ACCOUNT' needs to be specified inside .env file '{args.env}'."
            )
            sys.exit(1)
        if gmail_app_password is None:
            print(
                f"Error: 'GMAIL_APP_PASSWORD' needs to be specified inside .env file '{args.env}'."
            )
            sys.exit(1)

        send_email(
            sender=gmail_account,
            recipient=email,
            text=text,
            gmail_app_password=gmail_app_password,
        )

    sys.exit(0)
