import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime


class TournamentsScrapper:
    """
        utility class to retrieve data about chess tournaments from chess_arbiter and chess_manager websites 
    """
    @staticmethod
    def get_tournaments_chessmanager(url : str, name : str | None = "")->list:
        """
            Retrieve chess tournaments basic info from website with links leading to them
            
            -------
            params:
            - url (str) :  link to the page with all options set
            - name (str) : phrase that is checked if its contained in tournament's name category 
        
            -------
            Returns
            list of dictionaries having given fields:
            - link (str) : link to the tournament subpage
            - date (str) : date when tournament begins
            - name (str) : name of the tournament
            - city (str) : city of tournament where it takes place
            - country (str) : country in which tournament takes place 
            - type_and_players (str) : info about tournament tempo TODO: need to change that field for a more meaningfull one
        
        """        
        # lets define some lambdas 
        retrieve_website_body = lambda url : BeautifulSoup(
            requests.get(url).content, 
            'html.parser'
        )
        get_subpage = lambda page, element :  page.find(
                        name=element, 
                        attrs = {"class": "ui bottom attached fluid vertical menu"} 
                        ).find_all(
                            name="a", 
                            attrs = {"class": "tournament item"}
                        )
        element = "div"
        soup = retrieve_website_body(url)
        tournament_list = []
        # try to find if we have multiple subpages for our given URL
        # if yes we retrieve tournaments info from each  subpage 
        offsets = soup.find(name = element, attrs = {"class" : "ui pagination menu"})
        if offsets != None:
            for link in offsets.descendants: # for safety measures 
                if link.name == "a": 
                    page = retrieve_website_body("https://www.chessmanager.com"+link["href"])
                    anchors = get_subpage(page, element)                  
                    tournament_list = tournament_list + TournamentsScrapper.webscrapp_subpage(anchors, name=name)
        #otherwise we retrieve info from our main subpage
        else:
            anchors = get_subpage(soup, element=element )
            tournament_list = TournamentsScrapper.webscrapp_subpage(anchors , name=name)

        return tournament_list

    @staticmethod
    def webscrapp_subpage(anchors : BeautifulSoup, name : str | None = "")->list:
        """
            Retrieve tournament data from chessmanager subpage

            ------
            Params:
            - anchors (BeatifulSoup) : anchor to another subpage
            - name (str) default "" : name of tournament which we want to retrieve, 
              if no name is given, then it retrieves all 

            ------
            Returns 
            list of dictionaries from subpage having given fields:
            - link (str) : link to the tournament subpage
            - date (str) : date when tournament begins
            - name (str) : name of the tournament
            - city (str) : city of tournament where it takes place
            - country (str) : country in which tournament takes place 
            - type_and_players (str) : info about tournament tempo TODO: need to change that field for a more meaningfull one
        """
        tournament_list = []
        def format_date(date: str)->str:  
            date_divided = re.findall(pattern="\d+\.\d+|\d+", string=date)            
            if len(date_divided) == 3:
                return f"{date_divided[0]}.{date_divided[2]}" 
            return date
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
            "date" : format_date(data[0].replace("\xa0" , "")),
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
            Retrieve chess tournaments basic info from website with links leading to them
            
            -------
            Params:
            - url (str) :  link to the page with all options set
            
            -------
            Returns list of dictionaries having given fields:
            - link (str) : link to the tournament subpage
            - date (str) : date when tournament begins
            - name (str) : name of the tournament
            - city (str) : city of tournament where it takes place
            - country (str) : country in which tournament takes place 
            - type_and_players (str) : info about tournament tempo TODO: need to change that field for a more meaningfull one
        """
        def format_date(date: str )->str:
            curDT = datetime.now()
            new = curDT.strptime(date, "%d-%m")
            return f"{new.day:02d}.{new.month:02d}.{curDT.year}"
        def retrieve_rows(table_rows):
            tournament_list = []
            for i in range(0, len(table_rows)): # we iterate from one to ignore edge case when our first row is a table header
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
                            "date" : format_date(re.findall( "[0-9\-]+" ,table_data[0].text )[0]),
                            "name" : re.sub("\xa0", "", name),
                            "city" : city.split(" ")[0],
                            "country" : country,
                            "type_and_players" : chess_type 
                        })
                    except:
                        # print(table_data)
                        print("Something propably has gone wrong with aquiring columns")
                        
            print(f" chessarbiter {len(tournament_list)}")
            return tournament_list
       
        element  = "tr"
        page = requests.get(url)
        page = page.content
        soup = BeautifulSoup(page.decode("utf-8", "ignore"), 'html.parser')
        
        
        # retrieve all the tables with tournaments 
        table_rows_1 = soup.find_all(name=element, attrs = {"class" : "tbl1"})
        table_rows_2 = soup.find_all(name=element, attrs = {"class" : "tbl2"})

        return retrieve_rows(table_rows_1) + retrieve_rows(table_rows_2)
        
    