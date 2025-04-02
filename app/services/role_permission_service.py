import sqlalchemy as sql
import app.models as models

def add_permission_to_role(db: sql.orm.Session, role: models.Role, permission: models.Permission):
    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
        db.refresh(role)
    return role

def remove_permission_from_role(db: sql.orm.Session, role: models.Role, permission_id: int):
    role.permissions = [p for p in role.permissions if p.id != permission_id]
    db.commit()
