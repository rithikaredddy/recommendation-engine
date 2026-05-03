from fastapi import APIRouter, HTTPException, Request, status
from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId

from models.user import UserRegister, UserLogin, UserResponse
from middleware.auth import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
async def register(request: Request, user: UserRegister):
    db = request.app.state.db
    # Check if email exists
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = pwd_context.hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw,
        "rated_movies": [],
        "watch_history": [],
        "created_at": datetime.utcnow()
    }
    result = await db.users.insert_one(new_user)
    user_id = str(result.inserted_id)
    token = create_access_token({"sub": user_id, "username": user.username})

    return UserResponse(id=user_id, username=user.username, email=user.email, token=token)

@router.post("/login", response_model=UserResponse)
async def login(request: Request, credentials: UserLogin):
    db = request.app.state.db
    user = await db.users.find_one({"email": credentials.email})
    if not user or not pwd_context.verify(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    token = create_access_token({"sub": user_id, "username": user["username"]})
    return UserResponse(id=user_id, username=user["username"], email=user["email"], token=token)
