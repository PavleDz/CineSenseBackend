from pydantic import BaseModel
from typing import List


class UserRolesUpdate(BaseModel):
    role_ids: List[int]
