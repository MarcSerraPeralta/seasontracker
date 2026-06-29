# seasontracker

CLI tool that tracks new season releases of TV shows using TMDB.
It prints or sends an email if new seasons are available.


## Installation

This package can be installed from source using:
```
git clone git@github.com:MarcSerraPeralta/seasontracker.git
cd seasontracker/
pip install .
```

## Configuration

To configure season tracker, first store your TMDB API Read Access token in a `.env` file
```
# ~/.seasontracker
TMDB_TOKEN=...
```
and if you want to use the Gmail notification, also store:
```
# ~/.seasontracker
GMAIL_ACCOUNT=...
GMAIL_APP_PASSWORD=...
```
_Tip: use `chmod 600 ~/.seasontracker` so that only your user can read the file._

To specify the seasons to keep track of, create the following YAML:
```
# yaml_example.yaml
- user: marc
  email: marcserraperalta@gmail.com    # Optional, status will be sent through email
  37854:     # TMDBid from www.themoviedb.org/tv/37854
    name: One Piece
    last_watched_season: 1
  79141:
    name: Scissor Seven
    last_watched_season: 2
- user: someone else # if 'email' is not specified, status will be printed
  1:
    name: some name
    last_watched_season: 0
```

## Execution

To check if the Gmail notifications work, run to send a test email to `GMAIL_ACCOUNT`:
```
seasontracker
```
If the `.env` file is not stored in `~/.seasontracker`, specify its path with `--env`.

To print/send email with the status of new seasons, run:
```
seasontracker yaml_example.yaml
```
If the user has an email, the status will be sent by email, otherwise it will be printed.

To stay up to date with new releases, it is recommended to set up a `cron` job for `seasontracker`.

