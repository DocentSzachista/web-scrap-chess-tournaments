from pymongo import MongoClient
from pydantic import BaseModel, EmailStr, Field
from mailing import send_email
from bson import ObjectId
# TODO: checkout what to do with docker 
client = MongoClient()
db = client.email_newsletters

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Data(BaseModel):
    id : PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email : EmailStr
    tournament_name : str | None  =""
    tournament_tempo : str | None =""
    tournament_status : str | None = "PLANNED"
    country_state : str | None = ""
    tournament_city : str | None = ""
    # Inner class is used to define config for model 
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {

            "example": {

                "email": "jdoe@example.com",
                "tournament_name": "",
                "tournament_status": "PLANNED",
                "country_state": "DS",
                "tournament_city": ""
            }

        }