from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# -------------------------
# Employment Schemas
# -------------------------
class EmploymentInfoBase(BaseModel):
    company_name: str
    designation: str
    start_date: date
    end_date: Optional[date] = None
    is_current: bool


class EmploymentInfoCreate(EmploymentInfoBase):
    pass


class EmploymentInfoResponse(EmploymentInfoBase):
    id: int

    class Config:
        orm_mode = True


# -------------------------
# Bank Info Schemas
# -------------------------
class BankInfoBase(BaseModel):
    bank_name: str
    account_number: str
    ifsc: str
    account_type: str


class BankInfoCreate(BankInfoBase):
    pass


class BankInfoResponse(BankInfoBase):
    id: int

    class Config:
        orm_mode = True


# -------------------------
# User Schemas
# -------------------------
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address_line1: str
    city: str
    state: str
    pincode: str


class UserCreate(UserBase):
    employment: List[EmploymentInfoCreate]
    bank_info: List[BankInfoCreate]


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    employment: List[EmploymentInfoResponse]
    bank_info: List[BankInfoResponse]

    class Config:
        orm_mode = True
