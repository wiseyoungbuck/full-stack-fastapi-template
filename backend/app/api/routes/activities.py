from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
#from app.models import Activity, ActivityCreate, ActivityOut, ActivityUpdate

router = APIRouter()

