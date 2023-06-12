from pydantic import BaseModel
from typing import Optional, Any
from datetime import timedelta

class CommonResponseSchema(BaseModel):
    type: str
    status_code: int
    message: str
    data: Optional[Any]

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    access_expires: int = timedelta(minutes=480)
    refresh_expires: int = timedelta(days=1)