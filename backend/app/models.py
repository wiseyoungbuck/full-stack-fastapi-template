from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime

from .enums import FinancingType, PhoneType

from pydantic_extra_types.phone_numbers import PhoneNumber

from pydantic import ConfigDict


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
#    phones: list["Phone"] = Relationship(back_populates="user")
    emails: list["Email"] = Relationship(back_populates="user")
#    organization: Optional["Organization"] = Relationship(back_populates="members")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# # Shared properties
# class ItemBase(SQLModel):
#     title: str
#     description: str | None = None


# # Properties to receive on item creation
# class ItemCreate(ItemBase):
#     title: str


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     title: str | None = None  # type: ignore


# # Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     title: str
#     owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
#     owner: User | None = Relationship(back_populates="items")


# # Properties to return via API, id is always required
# class ItemOut(ItemBase):
#     id: int
#     owner_id: int


# class ItemsOut(SQLModel):
#     data: list[ItemOut]
#     count: int

# ------------------------ Organization Models  ------------------------------------


class OrganizationBase(SQLModel):
    name: str


class OrganizationCreate(OrganizationBase):
    model_config = ConfigDict(extra='ignore')
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationOut(OrganizationBase):
    id: int
    # phones: list["Phone"]
    emails: list["Email"]
    pass


class OrganizationsOut(SQLModel):
    data: list[OrganizationOut]
    count: int


class Organization(OrganizationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    # Non DB fields Useful for Pydantic/FastAPI/SQLModel
    # addresses: list[Address] = Relationship(back_populates="organization")
    emails: list["Email"] = Relationship(back_populates="organization")
    # phones: list["Phone"] = Relationship(back_populates="organization")
    # members: list[User] = Relationship(back_populates="organization")
    # owned_vehicles: list["Vehicle"] = Relationship(back_populates="organization")


# class OrganizationReadwithSalesPeople(OrganizationRead):
#     salespeople: list["SalesPersonRead"] = []


# ------------------------ Vehicle Models  ------------------------------------


class VehicleBase(SQLModel):
    vin: str
    financing_type: Optional[FinancingType] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    price: Optional[float] = None
    msrp: Optional[float] = None
    has_lien: Optional[bool] = None


class VehicleCreate(VehicleBase):
    organization_id: Optional[int] = None


class VehicleUpdate(VehicleBase):
    pass


class VehicleOut(VehicleBase):
    pass


class VehiclesOut(SQLModel):
    data: list[VehicleOut]
    count: int


# Database model
class Vehicle(VehicleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # prospect_id: Optional[int] = Field(default=None, foreign_key="prospect.id")
    # prospect: Optional[Prospect] = Relationship(back_populates="owned_vehicles")

    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    #organization: Optional[Organization] = Relationship(back_populates="owned_vehicles")

    # activity_id: Optional[int] = Field(default=None, foreign_key="activity.id")
    # activity: Optional[Activity] = Relationship(back_populates="recommended_vehicle")


# ------------------------ Phone Models  ------------------------------------
class Phone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: PhoneNumber
    phone_type: PhoneType
    is_primary: bool = False
    # user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # user: Optional[User] = Relationship(back_populates="phones")
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
#    organization: Optional["Organization"] = Relationship(back_populates="phones")

    # Non DB fields Useful for Pydantic/FastAPI/SQLModel
    # prospect_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # prospect: Optional["Prospect"] = Relationship(back_populates="phones")


# ------------------------ Email Models  ------------------------------------
class Email(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email_address: Optional[str] = None
    is_primary: Optional[bool] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="emails")
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    organization: Optional["Organization"] = Relationship(back_populates="emails")

    # prospect_id: Optional[int] = Field(default=None, foreign_key="prospect.id")
    # prospect: Optional["Prospect"] = Relationship(back_populates="emails")


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str
