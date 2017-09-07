# Trello Sorter
> A python2 command line tool for organizing trello cards

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```
usage: sort.py [-h] [-l] [-n] apikey

Interactive command line utility for sorting Trello lists

positional arguments:
  apikey         Trello API Key from https://trello.com/app-key

optional arguments:
  -h, --help     show this help message and exit
  -l, --label    label the cards based on classes using format "ECE 112:" or
                 "ECE112"
  -n, --no-sort  Disable sorting
```
