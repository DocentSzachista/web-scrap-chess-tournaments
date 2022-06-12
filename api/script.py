from mailing import parse_html_to_file , get_json_data
from webscrapping import URLConfigure, TournamentsScrapper
from main import data_retrieval_wrapper
from datetime import date, datetime

import subprocess

if __name__ == "__main__":
    config = get_json_data("userPreferences.json")
    
    for parameter in config:
        print(parameter)
        retrieved_data = data_retrieval_wrapper(  
            tournament_city = parameter["tournament_city"],
            country_state = parameter["country_state"],
            tournament_status = parameter["tournament_status"],
            tempo_option = parameter["tournament_tempo"],
            tournament_name = parameter["tournament_name"]
        )
        parse_html_to_file(parameter["country_state"], retrieved_data)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m" f'"Tournaments update {datetime.today()}"'])
    subprocess.run(["git", "push"])