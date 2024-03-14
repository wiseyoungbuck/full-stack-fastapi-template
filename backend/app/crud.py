from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Organization,
    OrganizationCreate,
    User,
    UserCreate,
    UserUpdate,
    Vehicle,
    VehicleCreate,
    VehicleUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj: User = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# def create_organization(*, session: Session, id: int) -> Organization:
#         db_org = Organization.model_validate(org_in)
#         session.add(db_org)
#         session.commit()
#         session.refresh(db_org)
#         return db_org
    
def get_organization_by_id(*, session: Session, id: int) -> Organization | None:
    statement = select(Organization).where(Organization.id == id)
    db_org: Organization | None = session.exec(statement).first()
    return db_org


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_vehicle(*, session: Session, vehicle_in: VehicleCreate, owner_id: int) -> Vehicle:
    db_vehicle: Vehicle = Vehicle.model_validate(vehicle_in, update={"owner_id": owner_id})
    session.add(db_vehicle)
    session.commit()
    session.refresh(db_vehicle)
    return db_vehicle

def get_vehicle_by_vin(*, session: Session, vin: str) -> Vehicle | None:
    statement = select(Vehicle).where(Vehicle.vin == vin)
    session_vehicle = session.exec(statement).first()
    return session_vehicle



