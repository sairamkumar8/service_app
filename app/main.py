from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas 
import crud
from database import engine, get_db


# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="CRUD operations for users, employment info, and bank info.",
    version="1.0",
)



# -----------------------------------------------------------
# 1. CREATE USER (with employment + bank info)
# -----------------------------------------------------------
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing = crud.get_users(db)  
    for u in existing:
        if u.email == user_in.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    user = crud.create_user(db, user_in)
    return user


# -----------------------------------------------------------
# 2. GET ALL USERS (with filters)
# -----------------------------------------------------------
@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(
    company: str | None = None,
    bank: str | None = None,
    pincode: str | None = None,
    db: Session = Depends(get_db)
):
    users = crud.get_users(db, company, bank, pincode)
    return users


# -----------------------------------------------------------
# 3. GET SINGLE USER
# -----------------------------------------------------------
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------------------------------------------------
# 4. UPDATE USER
# -----------------------------------------------------------
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_api(user_id: int, data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated



# -----------------------------------------------------------
# 5. DELETE USER
# -----------------------------------------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# -----------------------------------------------------------
# 6. ADD EMPLOYMENT RECORD FOR A USER
# -----------------------------------------------------------
@app.post("/users/{user_id}/employment", response_model=schemas.EmploymentInfoResponse)
def add_employment(user_id: int, emp_in: schemas.EmploymentInfoCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.add_employment(db, user_id, emp_in)


# -----------------------------------------------------------
# 7. ADD BANK RECORD FOR A USER
# -----------------------------------------------------------
@app.post("/users/{user_id}/bank", response_model=schemas.BankInfoResponse)
def add_bank(user_id: int, bank_in: schemas.BankInfoCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.add_bank(db, user_id, bank_in)

# 8. UPDATE EMPLOYMENT INFO FOR A USER
# ------------------------------------------------------------ 
@app.put("/employment/{emp_id}", response_model=schemas.EmploymentInfoResponse)
def update_employment_api(emp_id: int, emp_in: schemas.EmploymentInfoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_employment(db, emp_id, emp_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Employment record not found")
    return updated

