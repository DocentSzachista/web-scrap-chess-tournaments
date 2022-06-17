from mailing import parse_html_to_file , get_json_data
from webscrapping import URLConfigure, TournamentsScrapper
from main import data_retrieval_wrapper
from datetime import date, datetime
import subprocess
import json
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

def update_repository():

    config = get_json_data("userPreferences.json")
    
    tournaments = dict()
    for parameter in config:
        print(parameter)
        retrieved_data = data_retrieval_wrapper(  
            tournament_city = parameter["tournament_city"],
            country_state = parameter["country_state"],
            tournament_status = parameter["tournament_status"],
            tempo_option = parameter["tournament_tempo"],
            tournament_name = parameter["tournament_name"],
            divided= True
        )
        tournaments[parameter["country_state"]] = retrieved_data
    dump_score_to_file(tournaments, "../docs/htmlLists/tournaments.json")
    parse_html_to_file(parameter["country_state"], retrieved_data, style_link='<link rel="stylesheet" href="../table_styles.css">')
    subprocess.run(["git", "add", "../docs"])
    subprocess.run(["git", "commit", "-m" f'"Tournaments update {datetime.today()}"'])
    subprocess.run(["git", "push"])

    
if __name__ == "__main__":
    update_repository()

