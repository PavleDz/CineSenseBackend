import sqlalchemy as sql
from typing import List, Optional

import app.models as models
import app.schemas.role_schema as role_schema


def get_all_roles(db: sql.orm.Session) -> List[models.Role]:
    return db.query(models.Role).all()


def get_role_by_id(db: sql.orm.Session, role_id: int) -> Optional[models.Role]:
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_role(db: sql.orm.Session, role_data: role_schema.RoleCreate) -> models.Role:
    role = models.Role(
        name=role_data.name,
        description=role_data.description
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: sql.orm.Session, role_id: int, role_data: role_schema.RoleUpdate) -> Optional[models.Role]:
    role = get_role_by_id(db, role_id)
    if not role:
        return None

    role.name = role_data.name
    role.description = role_data.description
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: sql.orm.Session, role_id: int) -> bool:
    role = get_role_by_id(db, role_id)
    if not role:
        return False
    db.delete(role)
    db.commit()
    return True
