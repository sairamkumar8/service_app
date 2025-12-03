from sqlalchemy.orm import Session
import models
import schemas


# ---------------------------------------------------
# CREATE USER + nested employment + nested bank info
# ---------------------------------------------------
def create_user(db: Session, user_in: schemas.UserCreate):
    # 1. Create user row
    user = models.User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone=user_in.phone,
        address_line1=user_in.address_line1,
        city=user_in.city,
        state=user_in.state,
        pincode=user_in.pincode,
        created_at="NOW()"  # Optional: we can override in main.py or remove this
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # refresh to get user.id

    # 2. Insert all employment rows
    for emp in user_in.employment:
        employment = models.EmploymentInfo(
            user_id=user.id,
            company_name=emp.company_name,
            designation=emp.designation,
            start_date=emp.start_date,
            end_date=emp.end_date,
            is_current=emp.is_current
        )
        db.add(employment)

    # 3. Insert all bank records
    for bank in user_in.bank_info:
        bank_record = models.UserBankInfo(
            user_id=user.id,
            bank_name=bank.bank_name,
            account_number=bank.account_number,
            ifsc=bank.ifsc,
            account_type=bank.account_type
        )
        db.add(bank_record)

    db.commit()
    db.refresh(user)
    return user



# ---------------------------------------------------
# GET ALL USERS (with filters)
# ---------------------------------------------------
def get_users(db: Session, company=None, bank=None, pincode=None):
    query = db.query(models.User)

    # If filter by company
    if company:
        query = query.join(models.EmploymentInfo).filter(
            models.EmploymentInfo.company_name.ilike(f"%{company}%")
        )

    # If filter by bank
    if bank:
        query = query.join(models.UserBankInfo).filter(
            models.UserBankInfo.bank_name.ilike(f"%{bank}%")
        )

    # If filter by pincode
    if pincode:
        query = query.filter(models.User.pincode == pincode)

    return query.all()



# ---------------------------------------------------
# GET SINGLE USER BY ID
# ---------------------------------------------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



# ---------------------------------------------------
# UPDATE USER (only basic fields)
# ---------------------------------------------------
def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None

    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user



# ---------------------------------------------------
# DELETE USER (cascade delete affects child tables)
# ---------------------------------------------------
def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True



# ---------------------------------------------------
# ADD NEW EMPLOYMENT FOR USER
# ---------------------------------------------------
def add_employment(db: Session, user_id: int, emp_in: schemas.EmploymentInfoCreate):
    employment = models.EmploymentInfo(
        user_id=user_id,
        company_name=emp_in.company_name,
        designation=emp_in.designation,
        start_date=emp_in.start_date,
        end_date=emp_in.end_date,
        is_current=emp_in.is_current
    )
    db.add(employment)
    db.commit()
    db.refresh(employment)
    return employment



# ---------------------------------------------------
# ADD NEW BANK RECORD FOR USER
# ---------------------------------------------------
def add_bank(db: Session, user_id: int, bank_in: schemas.BankInfoCreate):
    bank = models.UserBankInfo(
        user_id=user_id,
        bank_name=bank_in.bank_name,
        account_number=bank_in.account_number,
        ifsc=bank_in.ifsc,
        account_type=bank_in.account_type
    )
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank
