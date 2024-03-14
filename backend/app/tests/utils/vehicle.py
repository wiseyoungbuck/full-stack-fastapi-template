from sqlmodel import Session

from app import crud
from app.models import Vehicle, VehicleCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_vehicle(db: Session) -> Vehicle:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    vin = random_lower_string()
    vehicle_in = VehicleCreate(vin=vin)
    return crud.create_vehicle(session=db, vehicle_in=vehicle_in, owner_id=owner_id)
