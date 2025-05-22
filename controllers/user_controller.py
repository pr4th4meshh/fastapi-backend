from fastapi import HTTPException
from models.user import UserCreate
from db.mongo import db
from datetime import datetime, timezone

users_collection = db["users"]
organizations_collection = db["organizations"]

async def create_user(user_data: UserCreate):
    user_dict = user_data.model_dump()

    # role check
    if user_dict["role"] == "team-member" and not user_dict.get("organizationName"):
        raise HTTPException(status_code=400, detail="Organization name is required for team-member")

    # check if organization exists
    if user_dict["role"] == "team-member":
        org = await organizations_collection.find_one({"organizationName": user_dict["organizationName"]})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

    user_dict["created_at"] = datetime.now(timezone.utc)
    user_dict["updated_at"] = datetime.now(timezone.utc)
    result = await users_collection.insert_one(user_dict)

    # add user to organization
    if user_dict["role"] == "team-member":
        await organizations_collection.update_one(
            {"organizationName": user_dict["organizationName"]},
            {"$push": {"users": result.inserted_id}}
        )

    # response to pass
    return {
        "message": "User created successfully",
        "userId": str(result.inserted_id)
    }
