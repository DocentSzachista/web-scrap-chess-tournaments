
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
    config = URLConfigure(tournament_city="", country_state="DS", tournament_status="PLANNED", tempo_option="classic")
    chess_arbiter = TournamentsScrapper.get_tournaments_chessarbiter(config.actual_link_arbiter)
    chess_manager = TournamentsScrapper.get_tournaments_chessmanager(config.actual_link_manager)
    chess_base = {
        "chess_arbiter": chess_arbiter,
        "chess_manager": chess_manager,
    }
    dump_score_to_file(chess_base)

    
