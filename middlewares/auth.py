from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from firebase_admin import firestore

security = HTTPBearer()

async def get_auth(request: Request, credentials: HTTPAuthorizationCredentials = security):
    token = credentials.credentials
    
    try:
        # decode and verify the token
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
    
        # get the user data from firestore
        doc = firestore.client().collection("users").document(uid).get()
        if not doc.exists:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        # get the user role
        user_data = doc.to_dict()
        role = user_data["role"]
        if not role:
            raise HTTPException(status_code=403, detail="User role not found")
        
        # set the user in the request state
        request.state.user = {
            "uid": uid,
            "role": role
        }
        
        
    except:
        raise HTTPException(status_code=403, detail="Unauthorized")