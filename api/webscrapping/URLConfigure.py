from base64 import encode
import urllib
class URLConfigure : 
    """
        Class that contains basic url options for chess arbiter and chess manager websites
    """


    COUNTRY_STATES =  { 
            "DS": ("DS", "Lower+Silesian+Voivodeship"),
            "KP": ("KP", "Kuyavian-Pomeranian+Voivodeship"),
            "LB": ("LB", "Lubusz+Voivodeship"),
            "LD": ("LD", "Łódź+Voivodeship"),
            "LU": ("LU", "Lublin+Voivodeship"),
            "MP": ("MP", "Lesser+Poland+Voivodeship"), # Małopolskie
            "MA": ("MA", "Masovian+Voivodeship"),# Mazowieckie
            "OP": ("OP", "Opole+Voivodeship"),# Opolske
            "PK": ("PK", "Podkarpackie+Voivodeship"),# Podkarpackie
            "PL": ("PL", "Podlaskie+Voivodeship"),# Podlaskie
            "PO": ("PO", "Pomeranian+Voivodeship"),# Pomorskie
            "SL": ("SL", "Silesian+Voivodeship"),# śląskie
            "SK": ("SK", "Swietokrzyskie"),# Swiętokrzyskie
            "WM": ("WM", "Warmian-Masurian+Voivodeship"),# Warminsko mazurskie
            "WP": ("WP", "Greater+Poland+Voivodeship"),# Wielkopolskie
            "ZP": ("ZP", "West+Pomeranian+Voivodeship")
        }
    TOURNAMENT_STATUS = {
        "PLANNED": ("planowane", "upcoming?"),
        "ONGOING": ("trwajace", "now?"),
        "FINISHED":("zakonczone", "finished?"),
        "ALL":     ("wszystkie", "now?")
    }
    TEMPO_OPTIONS = {
        "blitz" :  ("blyskawiczne", "blitz"),
        "rapid":   ("szybkie","rapid"),
        "classic": ("klasyczne","standard"),
    }
    # Basic link 
    CHESS_MANAGER_LINK = "https://www.chessmanager.com/pl/tournaments"
    CHESS_ARBITER_LINK = "http://www.chessarbiter.com/"

    def __init__(self) -> None:
        pass
        # create data query for url
        #  safe = :+ ignores encoding "+" signs as a %2f 
        
    def retrieve_chess_arbiter_link(self,
                    tournament_name = "",
                    tournament_city = "", 
                    tournament_speed = "", 
                    tournament_status = "ALL", 
                    country_state = "", 
                    tempo_option = ""   
        ) -> str:
        """
        Parameters
        ==========
            tournament_name (str) :, 
            tournament_city (str):,
            tournament_speed (str) : - option not implemented yet
            tournament_status (str) : one of option written as string (ALL, FINISHED, ONGOING, PLANNED),
            country_State (str) : polish shortcut of country state ex DS for "Lower Silesian State",
            
        """
        chess_arbiter_params = {
            "nazwa": tournament_name,
            "miejsce": tournament_city,
            "status": self.TOURNAMENT_STATUS[tournament_status][0] if tournament_status != "" else '',
            "wojewodztwo": self.COUNTRY_STATES[country_state][0] if country_state != "" else '',
            "typ": "wszystkie",
            "rodzaj": self.TEMPO_OPTIONS[tempo_option][0] if tempo_option != '' else 'wszystkie',
            "szukaj": "Wyswietl+turnieje" 
        }
        chess_arbiter_data = urllib.parse.urlencode(chess_arbiter_params, safe=":+")
        link = urllib.parse.urljoin(self.CHESS_ARBITER_LINK, f"index.php?{chess_arbiter_data}")
        # Potrzebne uzycie unquota by zastapic wyrażenia %xx na jego odpowiednik w znaku  
        return     urllib.parse.unquote(link)

    def retrieve_chess_manager_link(self, 
                    tournament_name = "",
                    tournament_city = "", 
                    tournament_speed = "", 
                    tournament_status = "ALL", 
                    country_state = "", 
                    tempo_option = ""  
        ) -> str:
        """
        Parameters
        ==========
            tournament_name (str) :, 
            tournament_city (str):,
            tournament_speed (str) : - option not implemented yet
            tournament_status (str) : one of option written as string (ALL, FINISHED, ONGOING, PLANNED),
            country_State (str) : polish shortcut of country state ex DS for "Lower Silesian State",
            
        """
        chess_manager_params = {
            "country" : "POL",
            "country_state":  self.COUNTRY_STATES[country_state][1] if country_state != "" else "all",
            "city": tournament_city, 
        }
        if tempo_option != '':
            chess_manager_params["tempo"] =  self.TEMPO_OPTIONS[tempo_option][1]
        chess_manager_data = urllib.parse.urlencode(chess_manager_params, safe=":+")

        # create links with data   
        return urllib.parse.urljoin(f"{self.CHESS_MANAGER_LINK}/", f"{self.TOURNAMENT_STATUS[tournament_status][1]}{chess_manager_data}")        