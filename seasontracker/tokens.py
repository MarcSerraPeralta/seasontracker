import os
import sys
import pathlib
import requests

TOKEN_DIR = pathlib.Path.home() / ".config" / "seasontracker"
TMDB_API_URL = "https://api.themoviedb.org/3"


def store_token(token: str, token_name: str, overwrite: bool = False) -> str | None:
    """Stores the token in TOKEN_DIR / token_name."""
    if not isinstance(token, str):
        raise TypeError(f"'token' must be a str, but {type(token)} was given.")
    if not isinstance(token_name, str):
        raise TypeError(
            f"'token_name' must be a str, but {type(token_name)} was given."
        )

    token_path = TOKEN_DIR / token_name
    token_path.parent.mkdir(exist_ok=True, parents=True)
    if token_path.exists() and not overwrite:
        return "FileExistsError"

    # create empty file and set permissions to 600 (owner read/write only)
    token_path.touch()
    os.chmod(token_path, 0o600)

    with open(token_path, "w") as file:
        _ = file.write(token)

    return


def get_token(token_name: str) -> tuple[str | None, str | None]:
    """Returns token stored in TOKEN_DIR / token_name."""
    token_path = TOKEN_DIR / token_name
    if not token_path.exists():
        return (None, "FileNotFoundError")

    with open(token_path, "r") as file:
        token = file.read()

    return (token, None)


def check_tmdb_token(token: object) -> None:
    if not isinstance(token, str):
        print(f"TMDB token must be a str, not {type(token)}.")
        sys.exit(1)

    # method to validate a TMDB token extracted from:
    # https://developer.themoviedb.org/docs/authentication-application
    url = f"{TMDB_API_URL}/movie/11"
    resp = requests.get(
        url,
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    if resp.status_code == 200:
        print("TMDB token is valid.")
        return
    else:
        print("TMDB token validation failed.")
        error = resp.json().get("status_message")
        print(f"Error {resp.status_code}: {error}")
        sys.exit(1)


def check_gmail_app_password(pwd: object) -> None:
    if not isinstance(pwd, str):
        print(f"Gmail app password must be a str, not {type(pwd)}.")
        sys.exit(1)
    return


def check_email(email: object) -> None:
    if not isinstance(email, str):
        print(f"Email must be a str, not {type(email)}.")
        sys.exit(1)
    if email.count("@") != 1:
        print("Email must contain only one '@'.")
        sys.exit(1)
    if email.split("@")[1] != "gmail.com":
        print("Email must end with 'gmail.com'.")
        sys.exit(1)
    return
