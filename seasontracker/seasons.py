from collections.abc import Generator

import sys
import requests
import yaml

from .tokens import TMDB_API_URL


def get_status(
    yaml_file: str, tmdb_token: str
) -> Generator[tuple[str, str | None, str], None, None]:
    with open(yaml_file, "r") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, list):
        print(f"YAML file must correspond to a list, not to {type(data)}.")
        sys.exit(1)

    for user_data in data:
        if not isinstance(user_data, dict):
            print(
                f"User data in YAML must correspond to a dict, not to {type(user_data)}."
            )
            sys.exit(1)

        if "user" not in user_data:
            print("'user' key must be in the YAML file for each user.")
            sys.exit(1)
        user = user_data.pop("user")

        email = None
        if "email" in user_data:
            email = user_data.pop("email")

        text = ""
        for tmdbid in user_data:
            if not isinstance(tmdbid, int):
                print("TMDBids in YAML file must be ints.")
                sys.exit(1)

            if "name" not in user_data[tmdbid]:
                name = f"TMDBid={tmdbid}"
            else:
                name = user_data[tmdbid]["name"]

            if "last_watched_season" not in user_data[tmdbid]:
                print(
                    "'last_watched_season' key must be in the YAML file for each user."
                )
                sys.exit(1)
            last_watched_season = user_data[tmdbid]["last_watched_season"]
            if not isinstance(last_watched_season, int):
                print("'last_watched_season' must be an int.")
                sys.exit(1)

            url = f"{TMDB_API_URL}/tv/{tmdbid}"
            resp = requests.get(
                url,
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {tmdb_token}",
                },
            )
            if resp.status_code != 200:
                print(f"Skipping TMDBid={tmdbid} due to bad answer from TMDB.")
                continue

            seasons = resp.json()["seasons"]
            next_seasons = [
                s["season_number"]
                for s in seasons
                if s["season_number"] == last_watched_season + 1
            ]
            if next_seasons:
                text += f"New season {min(next_seasons)} for {name}!\n"

        # remove last "\n" (if needed)
        if len(text) != 0:
            text = text[:-1]

        yield user, email, text
