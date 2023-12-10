from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from db import session, Person, get_user
from typing import Optional, Dict, Any

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@app.post("/register")
def register_user(data : Dict = Body(...)):
    
    username = data.get("username")
    password = data.get("password")

    # check that user does not exist
    user = get_user(username)
    if user is not None:
        raise HTTPException(status_code=400, detail="User with that username alredy exists")
    
    hashed_password = pwd_context.hash(password)
    
    # Save user to db
    person = Person(username, hashed_password)
    session.add(person)
    session.commit()
    
    return {"username": username, "hashed_password": hashed_password}



@app.post("/auth")
def authenticate_user(data : Dict = Body(...)):

    username = data.get("username")
    password = data.get("password")
    user = get_user(username)
    
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username")

    hashed_user_password = user.get("pass_hash")
    password_correct = pwd_context.verify(password, hashed_user_password)

    if not password_correct:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # jwt_token = create_jwt_token({"sub": username})
    return {"auth": "success", "username": username}

