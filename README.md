[![GitHub issues](https://img.shields.io/github/issues/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/issues)
[![GitHub forks](https://img.shields.io/github/forks/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/network)
[![GitHub stars](https://img.shields.io/github/stars/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/stargazers)
[![GitHub license](https://img.shields.io/github/license/DocentSzachista/web-scrap-chess-tournaments)](https://github.com/DocentSzachista/web-scrap-chess-tournaments/blob/master/LICENSE)
![PyPI - Python Version](https://img.shields.io/badge/python-3.10-blue)

# Chess tournaments webscrapper

This is a repository that contains scripts allowing to webscrap two chess tournaments webpages: 
- Chess arbiter : http://www.chessarbiter.com/
- Chess manager : https://www.chessmanager.com/pl/tournaments

# Table of contents 
- Webscrapping
   - How is data being scrapped
   - URL parameters
   - data retrieved
- Required packages
- How to install it 

# Websccrapping


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
  3. Add ``smtpServer.json`` with configurations for smpt server to project directory. Example file contents:

  ```
{
    "sender_email" : "example@gmail.com",
    "password": "example",
    "smtp_server": "smtp.gmail.com",
    "port" : 123
}
  ```

## requirements.txt content
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
