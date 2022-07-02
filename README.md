[![GitHub issues](https://img.shields.io/github/issues/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/issues)
[![GitHub forks](https://img.shields.io/github/forks/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/network)
[![GitHub stars](https://img.shields.io/github/stars/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/stargazers)
[![GitHub license](https://img.shields.io/github/license/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/blob/master/LICENSE)
![PyPI - Python Version](https://img.shields.io/badge/python-3.10-blue)
[![Update tournaments](https://github.com/DocentSzachista/web-scrap-chess-tournaments/actions/workflows/schedule.yml/badge.svg?branch=master)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/actions/workflows/schedule.yml)
# Chess tournaments webscrapper

This is a repository that contains scripts allowing to webscrap two chess tournaments webpages: 
- Chess arbiter : http://www.chessarbiter.com/
- Chess manager : https://www.chessmanager.com/pl/tournaments

# Table of contents 
- [Webscrapping](#webscrapping)
   - [URL parameters](#url-parameters)
   - [Webscrapped data structure](#webscrapped-data-structure)
- [How to install it](#how-to-install-it)
- [How to use it](#how-to-use-it)
  - [FastAPI](#fastapi)
  - [Automated script](#automated-script)
- [requirements.txt content](#requirementstxt-content)
- [Additional notes](#additional-informations)

# Webscrapping


## URL parameters
Each website have different named parameters but they actually allow for filter data in the same way.
### Example URL's:
 
  - Chessmanager: https://www.chessmanager.com/pl/tournaments/upcoming?country=POL&country_state=all&city=&city_radius=0&tempo=rapid
  - Chessarbiter: http://www.chessarbiter.com/index.php?nazwa=&miejsce=&status=wszystkie&wojewodztwo=wszystkie&typ=wszystkie&rodzaj=wszystkie&szukaj=Wyswietl+turnieje
 
### Division of url parameters
 - country  / filters by country (it has only parameter on chess manager because on chess arbiter tournaments exists only for Poland)
 - country_state / wojewodztwo - filter by country_state
 - city / miejsce - filter by city 
 - planned / status  - filter status of tournament, in case of chessmanager it displays as /planned, /now and /finished
 - tempo / typ - filter tournament speed 


## Webscrapped data structure

### Description of parameters:
- link: provides link to a subpage where we can sign for a tournament
- date: dependant on website, on chessarbiter it will display only date when its starts, when on chess manager it shows start and end dates.
- name: tournament title
- city: City where tournaments is being held.
- country:  Country in which tournament takes place
- type_and_players : displays tournament tempo. 

### JSON example for single tournament
```
{
         "link": "http://www.chessarbiter.com/turnieje/open.php?turn=2022/ti_2914&n=",
         "date": "01-06",
         "name": "Grand Prix Grzybowic z okazji 100 - lecia Miasta Zabrze Turniej 8 cykl II 2022r zgłoszony do Fide",
         "city": "Zabrze",
         "country": "Poland",
         "type_and_players": "SL blitz"
},
```
### Why only that data is being scrapped?
As intention of this script was just to automate my search for tournaments in my area, which I needed mostly info about: 
- When tournament takes place?
- Which city?
- What is tempo of that tournament?
- Link to be able for signup

# How to install it? 

1. Have installed at least python 3.10
2. Have installed mongo.db database
2. Create new virtual environment and install packages:
  - **Windows** 
```
  python -m venv your_env_name
``` 
```
  ./your_env_name/Scripts/activate
```
```
  pip install -r /path/to/requirements.txt
```
  - **Linux**   
```
  python3 -m venv your_env_name
``` 
```
  source ./your_env_name/bin/activate
```
```
  pip3 install -r /path/to/requirements.txt
```
 
# How to use it?
## FastAPI
 Add ``smtpServer.json`` with configurations for smpt server to project directory. Example file contents:
  ```
{
    "sender_email" : "example@gmail.com",
    "password": "example",
    "smtp_server": "smtp.gmail.com",
    "port" : 123
}
  ```
If you want to launch fastAPI server you only need to use command in project directory:
```
python3 main.py 
```  
## Automated script 
### How it works
Script webscrapps informations from websites and later saves them into tournaments.json file in `docs/htmlLists` directory. When its done it calls git commands to push changes into repository. Then the github pages are being rebuilt and when the process is done you can simply see data on [github pages](https://docentszachista.github.io/web-scrap-chess-tournaments/).
If you want to make it actually work I **recommend to fork repository**
### Required files to add
In order to make script work as intended, you need to add `userPreferences.json` file to your project directory.
It should contain following fields:
  -  `"tournament_name"` - signs which tournament name should contain
  -  `"tournament_tempo"` - speed in which tournament occurs
  -  `"tournament_status"` - tournament actual state. It can be: PLANNED, FINISHED, ONGOING, ALL
  -  `"country_state"` - country state that tournaments interest us
  -  `"tournament_city"` - city from which we would like to get info about tournaments 

Example file content: 
```
[
    {
        "tournament_name":"",
        "tournament_tempo":"",
        "tournament_status":"PLANNED",
        "country_state": "DS",
        "tournament_city":""
    },
    {
        "tournament_name":"",
        "tournament_tempo":"",
        "tournament_status":"PLANNED",
        "country_state": "LB",
        "tournament_city":""
    },
    {
        "tournament_name":"",
        "tournament_tempo":"",
        "tournament_status":"PLANNED",
        "country_state": "OP",
        "tournament_city":""
    },
    {
        "tournament_name":"",
        "tournament_tempo":"",
        "tournament_status":"PLANNED",
        "country_state": "WP",
        "tournament_city":""
    }
]
```


# requirements.txt content
```
urlib 
beatifulsoup
requests
fastapi
prettytable
mongoengine
pymongo
apscheduler
"uvicorn[standard]"
```
## Additional informations
You need to use another provider than google, because they have turned off their support for using gmail as SMTP service (but changing to other mail domain will work as well) at 30.05.2022 year
### UPDATE TO NOTE
Actually you can still use google, only what you need to do is to enable 2-factor authetincation which is described [here](https://stackoverflow.com/questions/72577189/gmail-smtp-server-stopped-working-as-it-no-longer-support-less-secure-apps) 
