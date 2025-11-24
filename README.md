# seasontracker

CLI tools that tracks new season releases of TV shows using TMDB.
It prints or sends an email if new seasons are available.


## Installation

This package can be installed from source using:
```
git clone git@github.com:MarcSerraPeralta/seasontracker.git
cd ..
pip install .
```

## Configuration

To configure season tracker, first specify your TMDB API Read Access token:
```
seasontracker login --tmdb-token <YOUR-TOKEN>
```
and if you want to use the Gmail notification, please specify:
```
seasontracker login --gmail-app-password <YOU-APP-PASSWORD>
seasontracker login --email <YOUR-EMAIL>
```

To specify the seasons to keep track of, create the following YAML:
```
- user: marc
  email: marcserraperalta@gmail.com    # Optional, required if using Gmail notifications
  37854:     # TMDBid from www.themoviedb.org/tv/37854
    name: One Piece
    last_watched_season: 1
  79141:
    name: Scissor Seven
    last_watched_season: 2
- user: someone else
  1:
    name: some name
    last_watched_season: 0
```

## Execution

To print the status of new seasons, run:
```
seasontracker status yaml_example.yaml
```
To receive an email notification about new seasons, run:
```
seasontracker notify yaml_example.yaml
```
To stay up to date with new releases, it is recommended to set up a `cron` job for `seasontracker`.

