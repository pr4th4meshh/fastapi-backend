from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class OrganizationBase(BaseModel):
    organizationName: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationInDB(OrganizationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    users: List[PyObjectId] = []
    gigs: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
