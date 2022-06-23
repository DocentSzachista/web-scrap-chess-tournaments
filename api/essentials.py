from webscrapping import URLConfigure, TournamentsScrapper
import json
url_config = URLConfigure()


def data_retrieval_wrapper(
    tournament_city : str | None = "", 
    country_state : str | None = "", 
    tournament_status : str | None = "PLANNED",
    tempo_option : str | None = "", 
    tournament_name : str | None ="",
    divided = False
)-> list:
    """
        function wrapper for filter and get requests
    """
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
    return  chess_manager +  chess_arbiter if not divided else {"chessarbiter" : chess_arbiter, "chessManager": chess_manager}

        
def dump_score_to_file(
        json_data: dict, 
        save_directory: str
    )->None:
    """
        saves formatted data to a json file

        Parameters
        ----------
        chess_base (dict) : tournament base to be saved 
    """
    with open(save_directory.format(1), "w", encoding="utf-8") as file: 
        json.dump(json_data, file, ensure_ascii=False, indent=3)
        file.close()


def get_json_data(filename : str) ->dict:
    """
        Retrieve config data for smtp server (email, pwd, port)
        -------
        Parameters
        - filename (str): link to json file 
        
        -------
        Returns
        dict with smtp server configuration.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)