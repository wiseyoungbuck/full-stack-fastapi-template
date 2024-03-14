from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app import crud
from app.models import Vehicle, VehicleCreate, VehicleOut, VehiclesOut, VehicleUpdate, Message, User, Organization

router = APIRouter()


@router.get("/", response_model=VehiclesOut)
def read_vehicles(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve vehicles.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Vehicle)
        count = session.exec(count_statement).one()
        statement = select(Vehicle).offset(skip).limit(limit)
        vehicles = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Vehicle)
            .where(Vehicle.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Vehicle)
            .where(Vehicle.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        vehicles = session.exec(statement).all()

    return VehiclesOut(data=vehicles, count=count)


@router.get("/{id}", response_model=VehicleOut)
def read_vehicle(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get vehicle by ID.
    """
    vehicle = session.get(Vehicle, id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not current_user.is_superuser and (vehicle.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return vehicle


@router.post("/", response_model=VehicleOut)
def create_vehicle(
    *, session: SessionDep, current_user: CurrentUser, vehicle_in: VehicleCreate
) -> Any:
    """
    Create new vehicle.
    """
    user: User | None = crud.get_user_by_email(session=session, email=current_user.email)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    vehicle: Vehicle | None = crud.get_vehicle_by_vin(session=session, vin=vehicle_in.vin)
    
    if vehicle_in.organization_id is not None:
        organization: Organization | None = crud.get_organization_by_id(session=session, id=vehicle_in.organization_id)
        if organization is None:
            raise HTTPException(status_code=400, detail=f"Organization with ID {vehicle_in.organization_id} not found")
    else:
        organization = None
    
    if vehicle is not None:
        raise HTTPException(status_code=400, detail=f"Vehicle with VIN {vehicle_in.vin} already exists")
    else:
        vehicle = crud.create_vehicle(session=session, vehicle_in=vehicle_in, owner_id=user.id)
    
        return vehicle


@router.put("/{id}", response_model=VehicleOut)
def update_vehicle(
    *, session: SessionDep, current_user: CurrentUser, id: int, vehicle_in: VehicleUpdate
) -> Any:
    """
    Update an vehicle.
    """
    vehicle = session.get(Vehicle, id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not current_user.is_superuser and (vehicle.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = vehicle_in.model_dump(exclude_unset=True)
    vehicle.sqlmodel_update(update_dict)
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.delete("/{id}")
def delete_vehicle(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an vehicle.
    """
    vehicle = session.get(Vehicle, id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not current_user.is_superuser and (vehicle.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(vehicle)
    session.commit()
    return Message(message="Vehicle deleted successfully")
