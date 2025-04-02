from pydantic import BaseModel
from typing import List


class RolePermissionsUpdate(BaseModel):
    permission_ids: List[int]
