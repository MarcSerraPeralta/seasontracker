import sys
import argparse

from .tokens import get_token, store_token, check_tmdb_token, TOKEN_DIR


def main():
    parser = argparse.ArgumentParser(prog="seasontracker")
    sub = parser.add_subparsers(dest="command")

    login = sub.add_parser("login", help="Store TMDB API token")
    login.add_argument("--tmdb-token", help="TMDB API Read Access token")
    login.add_argument("--overwrite", action="store_true", help="Overwrite token")

    status = sub.add_parser("status", help="Print status of TV shows")

    notify = sub.add_parser("notify", help="Sends status of TV shows via email")
    notify.add_argument("--app-password", help="Gmail App password to store")

    args = parser.parse_args()

    if args.command == "login":
        if args.tmdb_token is None:
            tmdb_token, _ = get_token("tmdb_api")
            if tmdb_token is None:
                print("Specify a TMDB API Read Access Token using:")
                print("")
                print("    seasontracker login --tmdb-token <YOUR-TOKEN>")
                print("")
                sys.exit(1)
            else:
                print("TMDB token has already been specified.")
                print("To overwrite it use:")
                print("")
                print("    seasontracker login --overwrite --tmdb-token <YOUR-TOKEN>")
                print("")
                sys.exit(1)

        check_tmdb_token(args.tmdb_token)
        error = store_token(args.tmdb_token, "tmdb_api", overwrite=args.overwrite)
        if error is None:
            print(f"TMDB token stored in {TOKEN_DIR / 'tmdb_api'}")
            sys.exit(0)
        elif error == "FileExistsError":
            print("TMDB token has already been specified.")
            print("To overwrite it use:")
            print("")
            print(f"    seasontracker login --overwrite --tmdb-token {args.tmdb_token}")
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
