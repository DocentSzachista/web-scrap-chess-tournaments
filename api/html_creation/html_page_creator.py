def generate_html_header(head_tags: str | None =""):
    return f"""
        <head>
            {head_tags}
        </head>
    """
def generate_html_body(data: list, table_fields: list | None = ["Date", "Name", "City", "Country", "Type"]  ):
    column_headers = "".join([f"\n\t\t\t\t\t<th>{header}</th>" for header in table_fields])
    table_rows = "".join(
        [
            f"""
            <tr onClick="linkOnClick('{data_row["link"]}')" >
              <td>{data_row["date"]}</td>
              <td>{data_row["name"]}</td>
              <td>{data_row["city"]}</td>
              <td>{data_row["country"]}</td>
              <td>{data_row["type_and_players"]}</td>
            </tr>
            """ for data_row in data 
        ]
    )
    return """
    <body>
        <table> 
            <thead> 
                <tr> %s \n \t\t\t\t</tr>
            </thead>
            <tbody>
                %s
            </tbody>
        </table>
        <script src="../script.js"></script>
    </body>
    """ % (column_headers, table_rows)
def generate_html_page(header, body):
    return """
        <html>
            %s
            %s 
        </html>
    """ % (header, body)


def parse_html_to_file(
    country_state : str, 
    data : list, 
    style_link : str | None = None, 
    table_fields: list | None = ["Date", "Name", "City", "Country", "Type"]
    ):
    
    header = generate_html_header(style_link) 
    body  =  generate_html_body(data, table_fields)
    html = generate_html_page(header, body)
    with open(f"../docs/htmlLists/{country_state}.html", "w", encoding="UTF-8") as file : 
        file.write(html)

