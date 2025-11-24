import sys
import argparse

from .tokens import (
    get_token,
    store_token,
    check_tmdb_token,
    check_gmail_app_password,
    check_email,
    TOKEN_DIR,
)
from .gmail import send_test_email


def main():
    parser = argparse.ArgumentParser(prog="seasontracker")
    sub = parser.add_subparsers(dest="command")

    login = sub.add_parser("login", help="Store TMDB API token and Gmail information")
    login.add_argument("--tmdb-token", help="TMDB API Read Access token")
    login.add_argument("--gmail-app-password", help="[Optional] Gmail App Password")
    login.add_argument("--email", help="[Optional] Gmail account")
    login.add_argument(
        "--send-test-email", action="store_true", help="Sends test email"
    )
    login.add_argument("--overwrite", action="store_true", help="Overwrite parameter")

    status = sub.add_parser("status", help="Print status of TV shows")

    notify = sub.add_parser("notify", help="Sends status of TV shows via email")

    args = parser.parse_args()

    if args.command == "login":
        if args.send_test_email:
            email, error1 = get_token("email")
            gmail_pwd, error2 = get_token("gmail_app_password")
            if (error1 is None) and (error2 is None):
                print(f"Sending test email to {email}...")
                send_test_email(email, gmail_pwd)
                print("Sent!")
                sys.exit(0)
            else:
                print("There has been a problem with the Gmail configuration. ")
                print("Run the following command for more information:")
                print("")
                print("    seasontracker login")
                print("")
                sys.exit(1)

        if (
            (args.tmdb_token is None)
            and (args.gmail_app_password is None)
            and (args.email is None)
        ):
            tmdb_token, _ = get_token("tmdb_api")
            gmail_pwd, _ = get_token("gmail_app_password")
            email, _ = get_token("email")
            if tmdb_token is None:
                print("Specify a TMDB API Read Access Token using:")
                print("")
                print("    seasontracker login --tmdb-token <YOUR-TOKEN>")
                print("")
                sys.exit(1)
            elif gmail_pwd is None:
                print("[Optional] Specify a Gmail App Password using:")
                print("")
                print(
                    "    seasontracker login --gmail-app-password <YOUR-APP-PASSWORD>"
                )
                print("")
                sys.exit(1)
            elif email is None:
                print("[Optional] Specify an email (Gmail) using:")
                print("")
                print("    seasontracker login --email <YOUR-EMAIL>")
                print("")
                sys.exit(1)
            else:
                print(
                    "TMDB token, Gmail app password, and email have already been specified."
                )
                print("To overwrite them use:")
                print("")
                print("    seasontracker login --overwrite --tmdb-token <YOUR-TOKEN>")
                print("")
                print("or")
                print("")
                print(
                    "    seasontracker login --overwrite --gmail-app-password <YOUR-APP-PASSWORD>"
                )
                print("")
                print("or")
                print("")
                print("    seasontracker login --overwrite --email <YOUR-EMAIL>")
                print("")
                sys.exit(1)

        if args.tmdb_token is not None:
            check_tmdb_token(args.tmdb_token)
            error = store_token(args.tmdb_token, "tmdb_api", overwrite=args.overwrite)
            if error is None:
                print(f"TMDB token stored in {TOKEN_DIR / 'tmdb_api'}")
                sys.exit(0)
            elif error == "FileExistsError":
                print("TMDB token has already been specified.")
                print("To overwrite it use:")
                print("")
                print(
                    f"    seasontracker login --overwrite --tmdb-token {args.tmdb_token}"
                )
                print("")
                sys.exit(1)
            else:
                print("Unknown error ocurred.")
                sys.exit(1)

        if args.gmail_app_password is not None:
            check_gmail_app_password(args.gmail_app_password)
            error = store_token(
                args.gmail_app_password, "gmail_app_password", overwrite=args.overwrite
            )
            if error is None:
                print(
                    f"Gmail app password stored in {TOKEN_DIR / 'gmail_app_password'}"
                )
                sys.exit(0)
            elif error == "FileExistsError":
                print("Gmail app password has already been specified.")
                print("To overwrite it use:")
                print("")
                print(
                    f"    seasontracker login --overwrite --gmail-app-password {args.gmail_app_password}"
                )
                print("")
                sys.exit(1)
            else:
                print("Unknown error ocurred.")
                sys.exit(1)

        if args.email is not None:
            check_email(args.email)
            error = store_token(args.email, "email", overwrite=args.overwrite)
            if error is None:
                print(f"Email stored in {TOKEN_DIR / 'email'}")
                sys.exit(0)
            elif error == "FileExistsError":
                print("Email has already been specified.")
                print("To overwrite it use:")
                print("")
                print(f"    seasontracker login --overwrite --email {args.email}")
                print("")
                sys.exit(1)
            else:
                print("Unknown error ocurred.")
                sys.exit(1)

    elif args.command == "status":
        print("NOT IMPLEMENTED")
        sys.exit(1)

    elif args.command == "notify":
        print("NOT IMPLEMENTED")
        sys.exit(1)

    else:
        print(f"Option '{args.command}' not found. See")
        print("")
        print("    seasontracker --help")
        print("")
        sys.exit(1)
