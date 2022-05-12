
from itertools import count
import json
from urllib import response
from webscrapping import URLConfigure, TournamentsScrapper
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

def dump_score_to_file(chess_base)->None:
    """
        saves formatted data to a json file

        Parameters
        ----------
        chess_base (dict) : tournament base to be saved 
    """
    def check_if_exists(database, value):
        for elem in database:
            if value in elem.values():
                return True
        return False

    # with open("data.json", "r", encoding="utf-8") as file:
    #     try: 
    #         old_content = json.load(file)
    #         file.close()
    #         for chess_element in chess_base["tournaments"]: 
    #             if not check_if_exists(old_content["tournaments"], chess_element["name"]):
    #                 new_content["tournaments"].append(chess_element)
    #         dupa_zmienna["tournaments"] =dupa_zmienna["tournaments"] + new_content
    #     except:
    #         print("No content")
    #     finally:    
    with open("Data.json".format(1), "w", encoding="utf-8") as file: 
        json.dump(chess_base, file, ensure_ascii=False, indent=3)
        file.close()




class Data(BaseModel):
    email : EmailStr
    tournament_name : str | None  =""
    tournament_tempo : str | None =""
    tournament_status : str | None = "PLANNED"
    country_state : str | None = ""
    tournament_city : str | None = ""



app = FastAPI()
url_config = URLConfigure()
def data_retrieval_wrapper(
    tournament_city : str | None = "", 
    country_state : str | None = "", 
    tournament_status : str | None = "PLANNED",
    tempo_option : str | None = "", 
    tournament_name : str | None =""
):
    chess_manager_link = url_config.retrieve_chess_manager_link(
        tournament_city=tournament_city, 
        country_state=country_state, 
        tournament_status=tournament_status,
        tempo_option=tempo_option
        )
    chess_arbiter_link = url_config.retrieve_chess_arbiter_link(
        tournament_name=tournament_name,
        tournament_city=tournament_city, 
        country_state=country_state, 
        tournament_status=tournament_status,
        tempo_option=tempo_option
        )
    chess_arbiter =  TournamentsScrapper.get_tournaments_chessarbiter(chess_arbiter_link)
    chess_manager = TournamentsScrapper.get_tournaments_chessmanager(chess_manager_link, name=tournament_name)
    return {
        "chess_manager": chess_manager, 
        "chess_arbiter": chess_arbiter,
    }

@app.get("/")
def retrieve_tournaments():
    """
        Retrieve tournaments without any desired options 
    """
    chess_base = data_retrieval_wrapper() 
    dump_score_to_file(chess_base)
    return chess_base


@app.get("/retrieve/filter/")
def filter_tournaments(
    tournament_city : str | None = "", 
    country_state : str | None = "", 
    tournament_status : str | None = "PLANNED",
    tempo_option : str | None = "", 
    tournament_name : str | None =""
    ):
    """
        Filter tournaments from given sites with desired options 
    """
    return data_retrieval_wrapper( tournament_city=tournament_city, 
        country_state=country_state, 
        tournament_status=tournament_status,
        tempo_option=tempo_option, 
        tournament_name=tournament_name)
   
@app.post("/addToMailingList/")
def add_user_to_mailing_list(user_preferences : Data):
    return user_preferences
