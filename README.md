# seasontracker

Tracks new season releases of TV shows using TMDB

This package is based on [seasonwatcher](https://github.com/gevhaz/seasonwatch).


## Installation

This package can be installed from source using:
```
git clone git@github.com:MarcSerraPeralta/seasontracker.git
pip install seasontracker/
```

## Configure

To configure season tracker, first specify your TMDB API Read Access token:
```
seasontracker login --tmdb-token <YOUR-TOKEN>
```
and if you want to use the Gmail notification, please specify:
```
seasontracker login --gmail-app-password <YOU-APP-PASSWORD>
seasontracker login --email <YOUR-EMAIL>
```
