from enum import Enum

class FinancingType(Enum):
    CASH: str = "Cash"
    FINANCE: str = "Finance"
    LEASE: str = "Lease"
    
class PhoneType(str, Enum):
    MOBILE: str = "mobile"
    HOME: str = "home"
    WORK: str = "work"