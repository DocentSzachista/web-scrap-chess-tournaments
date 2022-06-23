"use-strict"

const linkOnClick = ( link ) =>{
    location.href = link;
};

const addListeners = ()=>{
    const checkboxes = document.querySelectorAll(".website-checkbox");
    console.log(checkboxes);
    checkboxes.forEach(element =>{
        element.addEventListener("change", () => {
             element.parentElement.className =  element.checked ? "my-btn-checked my-btn-border" : "my-btn my-btn-border"
        });
    });
};

const goToTable = (key) =>{
    localStorage.setItem("key", key);
    checkCheckboxes();
    location.href = "./htmlLists/table.html";
};

const loadTable = () =>{
    const key = localStorage.getItem("key");
    retrieveFile(key);
};

const checkCheckboxes = () =>{
    const checkboxes = document.querySelectorAll('input[name="tournamentWebsite"]');
    const values = [];
    checkboxes.forEach((iterator) => { if(iterator.checked) values.push( iterator.value)} );
    localStorage.setItem("tournaments", values.length !==0? JSON.stringify(values) : JSON.stringify(["chessarbiter", "chessManager"]));
};

const sortSubArray = (subArray) =>{
    return subArray.sort( (a, b) =>{
        const dateA = new Date(a.date.split(".").reverse().join("-"));
        const dateB = new Date(b.date.split(".").reverse().join("-"));
        return dateA - dateB;  
    } );
}
const generateTableRow =(element) =>{
    const tableRow = document.createElement("tr");
    tableRow.onclick = () => linkOnClick(element.link);
    const rowValues = Object.values(element);
    rowValues.slice(1).forEach(property =>{
        const data = document.createElement("td");
        data.textContent = property;
        tableRow.appendChild(data);
    } );
    return tableRow
};

const generateTable = (dataToDisplay, displayOptions) =>{
    const tableBody = document.getElementById("table-body");
    if(tableBody.childNodes.length !==0){
        tableBody.innerHTML = "";
    }
    let tournaments = [];
    displayOptions.forEach( website => {
        tournaments = tournaments.concat(dataToDisplay[website]);    
    });
    const sorted =sortSubArray(tournaments); 
    sorted.forEach(element => {
            tableBody.appendChild(
                generateTableRow(element)
            );
        });
};

const  retrieveFile = async (country_state) =>{
    const response = await fetch("./tournaments.json", {headers:{
        'Access-Control-Allow-Origin': '*',
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }});
    if(response.ok){
        const dataToDisplay = await response.json();
        generateTable(
            dataToDisplay[country_state], 
            JSON.parse(localStorage.getItem("tournaments"))
        );
    }
    else
        console.error("Something went wrong with reading data from json");
};
