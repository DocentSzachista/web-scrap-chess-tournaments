
from base64 import encode
from webscrapping import URLConfigure, TournamentsScrapper
import json



def dump_score_to_file(chess_base)->None:
    """
        saves formatted data to a json file

        Parameters
        ----------
        chess_base (dict) : tournament base to be saved 
    """
    with open("Data.json".format(1), "w", encoding="utf-8") as file: 
        json.dump(chess_base, file, ensure_ascii=False, indent=3)


if __name__ == "__main__":
    
    printer = lambda els : [print(f"{x} \n" ) for x in els]
    config = URLConfigure()
    
    chess_arbiter = TournamentsScrapper.get_tournaments_chessarbiter(config.retrieve_chess_arbiter_link(tournament_city="Poznań", country_state="", tournament_status="PLANNED", tempo_option=""))
    chess_manager = TournamentsScrapper.get_tournaments_chessmanager(config.retrieve_chess_manager_link(tournament_city="Wroclaw", country_state="", tournament_status="PLANNED", tempo_option=""))
    chess_base = {
        "chess_manager": chess_manager,
        "chess_arbiter": chess_arbiter,
    }
    dump_score_to_file(chess_base)

    
