from mailing import send_email
from essentials import data_retrieval_wrapper
from db_mongo import db, Data
from typing import List
import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

def  send_mails():
    users =  get_mailing_list() 
    for user in users:
        
        data = data_retrieval_wrapper(
            tournament_city=user["tournament_city"], 
            tournament_status=user["tournament_status"],
            tempo_option=user["tournament_tempo"],
            country_state=user["country_state"],
            tournament_name=user["tournament_name"]
            )
        send_email(user["email"], data )


app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def schedule_mail_sender():
    """
        Background scheduler that launches each 7 days function to send mails
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job( send_mails , "interval", seconds=7) 
    scheduler.start()


@app.get(
    "/", 
    response_description=" Retrieve tournaments without any desired options ",
    
)
async def retrieve_tournaments():
    chess_base = data_retrieval_wrapper() 
    return chess_base

@app.get(
    "/retrieve/filter/", 
    response_description="Filter tournaments from given sites with desired options",
)
async def filter_tournaments(
    tournament_city : str | None = "", 
    country_state : str | None = "", 
    tournament_status : str | None = "PLANNED",
    tempo_option : str | None = "", 
    tournament_name : str | None =""
    ):
    return data_retrieval_wrapper( tournament_city=tournament_city, 
        country_state=country_state, 
        tournament_status=tournament_status,
        tempo_option=tempo_option, 
        tournament_name=tournament_name)

"""
CRUD SECTION : 
"""

@app.post(
    "/addToMailingList/",
    response_description = "Add user to a newsletter",
    response_model = Data
)
async def add_user_to_mailing_list(subscription : Data):
    subscription = jsonable_encoder(subscription)
    do_exists = db["mailings"].find_one({"email": subscription["email"]})
    if not do_exists :
        new_item =  db["mailings"].insert_one(subscription)
        created_mailing =  db["mailings"].find_one({"_id": new_item.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_mailing)

    raise HTTPException(status_code=409, detail=f"Given mail already signed up for a newsletter")

@app.get(
    "/getMailingList/",
    response_description = "Get all newsletters",
    response_model = List[Data]
)
def get_mailing_list():
    mailings = list(db["mailings"].find({}))
    return mailings

@app.delete(
    "/{id}",
    response_description = "Delete from mailing list"
)
async def delete_from_mailing_list(id: str):
    delete_result = db["mailings"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Mailing not found")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True, debug=False)
