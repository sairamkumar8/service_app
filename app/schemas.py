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
# Employment Update Schema
# -------------------------
class EmploymentInfoUpdate(BaseModel):
    company_name: str | None = None
    designation: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    class Config:
        from_attributes = True

class EmploymentInfoUpdateFull(BaseModel):
    id: int
    company_name: str | None = None
    designation: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    class Config:
        from_attributes = True
        
# -------------------------
# Bank Info Schemas
# -------------------------
class BankInfoBase(BaseModel):
    bank_name: str
    account_number: str
    ifsc: str
    account_type: str

class BankInfoUpdateFull(BaseModel):
    id: int
    bank_name: str | None = None
    account_number: str | None = None
    ifsc: str | None = None
    account_type: str | None = None

    class Config:
        from_attributes = True



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


class UserUpdate(BaseModel):
    # basic user fields (optional)
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address_line1: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None

    # nested updates
    employment: list[EmploymentInfoUpdateFull] | None = None
    bank_info: list[BankInfoUpdateFull] | None = None

    class Config:
        from_attributes = True



class UserResponse(UserBase):
    id: int
    employment: List[EmploymentInfoResponse]
    bank_info: List[BankInfoResponse]

    class Config:
        orm_mode = True
