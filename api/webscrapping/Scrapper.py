import requests
import re
from bs4 import BeautifulSoup
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
    @staticmethod
    def get_chessarbiter_subpage(url : str)->list:
        raise NotImplementedError("Function not implemented yet")
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
