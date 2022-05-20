import requests
import re
from bs4 import BeautifulSoup
class TournamentsScrapper:
    """
        utility class to retrieve data about chess tournaments from chess_arbiter and chess_manager websites 
    """
    @staticmethod
    def get_tournaments_chessmanager(url : str, name : str | None = "")->list:
        """
            Retrieve chess tournaments basic info from website with links leading to them
            
            params:
            -------
            - url (str) : link to the page with all options set
            - name (str) : 
        """
        #TODO: Add support for multipages 
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
            if name.lower() not in data[2].lower() and name != "":
                continue 
            # Add tournament info to list 
            tournament_list.append({
            "link" : f" https://www.chessmanager.com{anchor['href']}",
            "date" : data[0].replace("\xa0" , ""),
            # "rounds" : data[1].replace("0/" , ""), 
            "name": data[2],
            "city": city,
            "country": country,
            "type_and_players": data[3].split(":")[0],  
            })

        return tournament_list

    @staticmethod
    def get_tournaments_chessarbiter(url)->list:
        """
            Retrieve data from chessarbiter website 
        """
        element  = "table"
        page = requests.get(url)
        page = page.content
        soup = BeautifulSoup(page.decode("utf-8", "ignore"), 'html.parser')
        tournament_list = []

        # retrieve all the tables with tournaments 
        tables = soup.find_all(name=element, attrs = {"style" : "tbl", "width" : "100%"})
        #print(tables[0].prettify())
        # lets locate all the table rows containing data 
        for table in tables : 
            # aquiring columns 
            table_rows = table.find_all(name="tr")
            for i in range(1, len(table_rows)): # we iterate from one to ignore edge case when our first row is a table header
                table_data = table_rows[i].find_all(name="td")    
                try: # neuragical part of code 
                    link =  table_data[1].find("a")
                    name, city = table_data[1].text.split("\n")
                    third_column =  table_data[2].text.split(",")
                    country = third_column[0] 
                    if len(third_column) == 3:
                        chess_type = third_column[2]
                    else:
                        chess_type = third_column[1]
                    tournament_list.append({
                        "link" : link["href"],
                        "date" : re.findall( "[0-9\-]+" ,table_data[0].text )[0],
                        "name" : re.sub("\xa0", "", name),
                        "city" : city.split(" ")[0],
                        "country" : country,
                        "type_and_players" : chess_type 
                    })
                except:
                    print("Something propably has gone wrong with aquiring columns")
        return tournament_list
    