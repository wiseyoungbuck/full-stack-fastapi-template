from fastapi import APIRouter

from app.api.routes import login, users, utils, vehicles, organizations, activities, prospects

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(prospects.router, prefix="/prospects", tags=["prospects"])
