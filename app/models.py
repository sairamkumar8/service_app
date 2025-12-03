from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# --------------------
# Users Table
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    address_line1 = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    created_at = Column(String)

    # relationships (one-to-many)
    employment = relationship("EmploymentInfo", back_populates="user", cascade="all, delete")
    bank_info = relationship("UserBankInfo", back_populates="user", cascade="all, delete")


# --------------------
# Employment Info Table
# --------------------
class EmploymentInfo(Base):
    __tablename__ = "employment_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String)
    designation = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean)

    # relationship back to user
    user = relationship("User", back_populates="employment")


# --------------------
# User Bank Info Table
# --------------------
class UserBankInfo(Base):
    __tablename__ = "user_bank_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bank_name = Column(String)
    account_number = Column(String)
    ifsc = Column(String)
    account_type = Column(String)

    # relationship back to user
    user = relationship("User", back_populates="bank_info")
