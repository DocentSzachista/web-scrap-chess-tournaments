from essentials import data_retrieval_wrapper, dump_score_to_file, get_json_data
from mailing import send_email
import argparse
def update_repository(file_dir: str):
    config = get_json_data(file_dir)
    tournaments = dict()
    for parameter in config:
        print(parameter)
        retrieved_data = data_retrieval_wrapper(  
            tournament_city = parameter["tournament_city"],
            country_state = parameter["country_state"],
            tournament_status = parameter["tournament_status"],
            tempo_option = parameter["tempo_option"],
            tournament_name = parameter["tournament_name"],
            divided= True
        )
        tournaments[parameter["country_state"]] = retrieved_data
    dump_score_to_file(tournaments, "./docs/htmlLists/tournaments.json")

def send_mailing_list(file_dir: str):
    preferences = get_json_data(file_dir)
    for user in preferences:
        data = data_retrieval_wrapper(
            **user["preferences"]
        )
        send_email(user["user"], data, config_file="api/smtpServer.json")

OPTIONS = {
    "mailing": send_mailing_list,
    "repository": update_repository
}
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", choices=["repository", "mailing"], type=str, help="Choose which program you wish to run")
    parser.add_argument("file_directory", type=str, help="directory to config file from which information will be retrieved to webscrapp data")
    args = parser.parse_args()
    OPTIONS[args.program](args.file_directory)
