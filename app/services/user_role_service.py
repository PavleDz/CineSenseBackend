import sqlalchemy as sql
import app.models as models

def add_role_to_user(db: sql.orm.Session, user: models.User, role: models.Role):
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    return user

def remove_role_from_user(db: sql.orm.Session, user: models.User, role_id: int):
    user.roles = [r for r in user.roles if r.id != role_id]
    db.commit()
