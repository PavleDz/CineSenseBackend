import sqlalchemy as sql
from sqlalchemy import select
from typing import List, Optional

import app.models as models
import app.schemas.permission_schema as permission_schema


def get_all_permissions(db: sql.orm.Session) -> List[models.Permission]:
    stmt = select(models.Permission)
    return db.execute(stmt).scalars().all()

def get_permission_by_id(db: sql.orm.Session, permission_id: int) -> Optional[models.Permission]:
    stmt = select(models.Permission).where(models.Permission.id == permission_id)
    return db.execute(stmt).scalar_one_or_none()

def create_permission(db: sql.orm.Session, data: permission_schema.PermissionCreate) -> models.Permission:
    permission = models.Permission(name=data.name, description=data.description)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def update_permission(db: sql.orm.Session, permission_id: int, data: permission_schema.PermissionUpdate) -> Optional[models.Permission]:
    perm = get_permission_by_id(db, permission_id)
    if not perm:
        return None
    perm.name = data.name
    perm.description = data.description
    db.commit()
    db.refresh(perm)
    return perm

def delete_permission(db: sql.orm.Session, permission_id: int) -> bool:
    perm = get_permission_by_id(db, permission_id)
    if not perm:
        return False
    db.delete(perm)
    db.commit()
    return True
