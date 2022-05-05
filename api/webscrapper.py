
import requests
import re
from bs4 import BeautifulSoup
import json
class URLConfigure : 
    """
        Class that contains basic url options for chess arbiter and chess manager websites
    """


    COUNTRY_STATES =  { 
            "DS": ("DS", "Lower+Silesian+Voivodeship"),
            "KP": ("KP", "Kuyavian-Pomeranian+Voivodeship"),
            "LB": ("LB", "Lubusz+Voivodeship"),
            "LD": ("LD", "Łódź+Voivodeship"),
            "LU": ("LU", "Lublin+Voivodeship"),
            "MP": ("MP", "Lesser+Poland+Voivodeship"), # Małopolskie
            "MA": ("MA", "Masovian+Voivodeship"),# Mazowieckie
            "OP": ("OP", "Opole+Voivodeship"),# Opolske
            "PK": ("PK", "Podkarpackie+Voivodeship"),# Podkarpackie
            "PL": ("PL", "Podlaskie+Voivodeship"),# Podlaskie
            "PO": ("PO", "Pomeranian+Voivodeship"),# Pomorskie
            "SL": ("SL", "Silesian+Voivodeship"),# śląskie
            "SK": ("SK", "Swietokrzyskie"),# Swiętokrzyskie
            "WM": ("WM", "Warmian-Masurian+Voivodeship"),# Warminsko mazurskie
            "WP": ("WP", "Greater+Poland+Voivodeship"),# Wielkopolskie
            "ZP": ("ZP", "West+Pomeranian+Voivodeship")
        }
    TOURNAMENT_STATUS = {
        "PLANNED": ("planowane", "upcoming?"),
        "ONGOING": ("trwajace", "now?"),
        "FINISHED":("zakonczone", "finished?"),
        "ALL":     ("wszystkie", "now?")
    }
    TEMPO_OPTIONS = {
        "blitz" :  ("blyskawiczne", "blitz"),
        "rapid":   ("szybkie","rapid"),
        "classic": ("klasyczne","standard"),
    }
    # Basic link 
    CHESS_MANAGER_LINK = "https://www.chessmanager.com/pl/tournaments"
    CHESS_ARBITER_LINK = "http://www.chessarbiter.com/index.php"

    def __init__(self, 
                    tournament_name = "",
                    tournament_city = "", 
                    tournament_speed = "", 
                    tournament_status = "ALL", 
                    country_state = "", 
                    tempo_option = ""  ) -> None:
        # "https://www.chessmanager.com/pl/tournaments/upcoming?country=POL&country_state=Lower+Silesian+Voivodeship&city=&city_radius=0"
        # "http://www.chessarbiter.com/index.php?nazwa=&miejsce=&status=planowane&wojewodztwo=DS&typ=wszystkie&rodzaj=wszystkie&szukaj=Wyswietl+turnieje"
        tempo_manager = f'&tempo={self.TEMPO_OPTIONS[tempo_option][1]}' if tempo_option != '' else ''
        print(tempo_manager) 
        state  = self.COUNTRY_STATES[country_state] if country_state != "" else ''
        self.actual_link_manager = f"{self.CHESS_MANAGER_LINK}/{self.TOURNAMENT_STATUS[tournament_status][1]}country=POL&country_state={state[1]}{f'&city={tournament_city}' if tournament_city !='' else '' }{tempo_manager}"
        self.actual_link_arbiter = f"{self.CHESS_ARBITER_LINK}?nazwa={tournament_name}&miejsce={tournament_city}&status={self.TOURNAMENT_STATUS[tournament_status][0]}&wojewodztwo={state[0]}&typ=wszystkie&rodzaj={ self.TEMPO_OPTIONS[tempo_option][0] if tempo_option != '' else 'wszystkie' }&szukaj=Wyswietl+turnieje"
        


class TournamentsScrapper:

    @staticmethod
    def get_tournaments_chessmanager(url)->list:
        """
            Retrieve chess tournaments basic info from website with links leading to them
        """
        element = "div"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tournament_list = []
        div = soup.find(name=element, attrs = {"class": "ui bottom attached fluid vertical menu"} )
        anchors = div.find_all(name="a", attrs = {"class": "tournament item"})

        for anchor in anchors :
            # Retrieve text and clean it from white signs and reformat so its easy to split up meaningfull data
            text = anchor.text    
            formatted_text = re.sub( "\s\s\s+", "   ",text.replace('\n', '').strip())
            data = formatted_text.split("   ")
            city, country = data[4].split(", ")

            # Add tournament info to list 
            tournament_list.append({
            "link" : f" https://www.chessmanager.com{anchor['href']}",
            "date" : data[0].replace("\xa0" , ""),
            # "rounds" : data[1].replace("0/" , ""), 
            "name": data[2],
            "type_and_players": data[3].split(":")[0],
            "city": city,
            "country": country  })

        return tournament_list

    @staticmethod
    def get_tournaments_chessarbiter(url)->list:
        """
            Retrieve data from chessarbiter website 

        """
        element  = "table"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tournament_list = []

        # retrieve all the tables with tournaments 
        tables = soup.find_all(name=element, attrs = {"style" : "tbl", "width" : "100%"})
        # lets locate all the table rows containing data 
        for table in tables : 
                
        #   get the columns yay
            table_rows = table.find_all(name="tr")
            for i in range(0, len(table_rows)):
                
                table_data = table_rows[i].find_all(name="td")
                if len(table_data) != 3 : # if we get table row without full data, its not worth our time then 
                    continue
                link =  table_data[1].find("a")
                #get_chessarbiter_subpage(link["href"])
                # print(link)
                name, city = table_data[1].text.split("\n")
                country, chess_type =  table_data[2].text.split(",")
                tournament_list.append({
                    "link" : link["href"],
                    "date" : re.findall( "[0-9\-]+" ,table_data[0].text )[0],
                    "name" : re.sub("\xa0", "", name),
                    "city" : city.split(" ")[0],
                    "country" : country,
                    "type_and_players" : chess_type 
                })
        return tournament_list
    # print(f"Wykryto turnieji :{len(tournament_list)}" )
    # @staticmethod
    # def get_chessarbiter_subpage(url : str)->list:
    #     # TODO: find info how to load after js scripts load site contents
    #  find a way 
    #     url = url.replace("&amp;n=", "/") 
    #     url = re.sub("[a-z]\w+.\w+\?[a-z]\w+\=", "", url)
    #     element = "td"
    #     #print(url)
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     print(soup.prettify())
    #     # sensitive_data_list = []
    #     # print(page.content)
    #     b_elem = soup.find_all(name="td", attrs={"class": "panel-body"})
    #     print(b_elem)


if __name__ == "__main__":
    printer = lambda els : [print(f"{x} \n" ) for x in els]
    URL_arbiter  = "http://www.chessarbiter.com/index.php?nazwa=&miejsce=&status=planowane&wojewodztwo=DS&typ=wszystkie&rodzaj=wszystkie&szukaj=Wyswietl+turnieje"
    URL_manager = "https://www.chessmanager.com/pl/tournaments/upcoming?country=POL&country_state=Lower+Silesian+Voivodeship&city=Wrocław&tempo=standard"

    test_url = "http://www.chessarbiter.com/turnieje/open.php?turn=2022/ti_2194&amp;n="

    config = URLConfigure(tournament_city="Wrocław", country_state="DS", tournament_status="FINISHED", tempo_option="classic")
    print(config.actual_link_manager)
    chess_arbiter = TournamentsScrapper.get_tournaments_chessarbiter(config.actual_link_arbiter)
    chess_manager = TournamentsScrapper.get_tournaments_chessmanager(config.actual_link_manager)
    # print(len(chess_arbiter))
  
    # printer(chess_arbiter) 
    
    printer(chess_manager)
    # chess_arbiter = TournamentsScrapper.get_tournaments_chessarbiter(URL_arbiter)
    # 
    # printer(chess_arbiter)
    # print( "\n", len(chess_manager))
    # chess_base = {
    #     "chess_arbiter": chess_arbiter,
    #     "chess_manager": chess_manager,
    # }
    # with open("Data.json".format(1), "w", encoding="utf-8") as file:
    #     json.dump(chess_base, file, ensure_ascii=False)

