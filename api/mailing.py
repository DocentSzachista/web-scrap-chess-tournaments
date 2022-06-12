
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from prettytable import PrettyTable
import json

def generate_table(data : list, fields : list)->PrettyTable: 
    """
        Create HTML table basing on given data 

        -------
        Params:
        - data ( list(str) ): rows of data that we want to parse to table
        - fields ( list ): column names

        --------
        Returns: PrettyTable object 

    """
    table  = PrettyTable(field_names=fields)
    for row in data :
        table.add_row(list(row.values()))
    return table

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

def generate_header()->str:
    """
        Retrieve styles for table 
    """
    return """
        <head>
            <style>
            table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }
            table th,
            table td {
                padding: 12px 15px;
            }
            table tbody tr {
                border-bottom: 1px solid #dddddd;
            }

            table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }

            table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }
        </style>
    </head>
    """

def generate_html_body(table: str) ->str: 
    """
        Generate email's html body

        ------
        Params:
        table (str): html table with data

        ------
        Returns:
        - str : fully structurized HTML table
    """
    return """
    <html>
         %s
        <body> 
            <div>
                <h3>Here is your data about tournaments</h3> 
                %s
            </div>
        </body>
    </html>
    """ % (generate_header(), table)

def send_email(receiver_email : str, data : list, table_fields: list | None = ["Link", "Date", "Name", "City", "Country", "Type"],  config_file: str | None = "smtpServer.json", ):

    """
        Send email with tournaments info 

        -------
        Params:
        - receiver_email (list):  list of emails that are to receive an email
        - data (list): List of data to display in a table
        - table_fields (list) :  coresponding columns labels for data, if none provided using default
        - config_file (str) : path to smtp server config file, it must be in JSON format.

        ------
        Returns:
          Nothing 
    """

    sender_data = get_json_data(config_file)
    table = generate_table(data, table_fields)

    html = generate_html_body(table.get_html_string())
    with open(f"../htmlLists/{receiver_email}.html", "w") as file : 
        file.write(html)

    # email_html_message = MIMEMultipart()
    # email_html_message["From"] = sender_data["sender_email"]
    # email_html_message["to"] = "".join(receiver_email)
    # email_html_message["Subject"] = "Chess tournaments newsletter"
    # email_html_message.attach(MIMEText(html, "html"))
    # email_string = email_html_message.as_string()
    # # context = ssl.create_default_context()
    # # with smtplib.SMTP_SSL(sender_data["smtp_server"], sender_data["port"], context=context) as server:
    # #     server.login(sender_data["sender_email"], sender_data["password"])
    # #     server.sendmail(sender_data["sender_email"], receiver_email, email_string)

def parse_html_to_file(country_state : str, data : list, table_fields: list | None = ["Link", "Date", "Name", "City", "Country", "Type"]):
    table = generate_table(data, table_fields)

    html = generate_html_body(table.get_html_string())
    with open(f"../htmlLists/{country_state}.html", "w") as file : 
        file.write(html)