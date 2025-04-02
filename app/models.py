import datetime
import sqlalchemy as sql
import app.database as database

Base = sql.orm.declarative_base()

# Konekcione
user_roles = sql.Table(
    'user_roles', Base.metadata,
    sql.Column('user_id', sql.ForeignKey('users.id'), primary_key=True),
    sql.Column('role_id', sql.ForeignKey('roles.id'), primary_key=True)
)

role_permissions = sql.Table(
    'role_permissions', Base.metadata,
    sql.Column('role_id', sql.ForeignKey('roles.id'), primary_key=True),
    sql.Column('permission_id', sql.ForeignKey('permissions.id'), primary_key=True)
)


# Povezana na role preko user_roles
class User(Base):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    username = sql.Column(sql.String(100), unique=True, index=True, nullable=False)
    email = sql.Column(sql.String(100), unique=True, index=True, nullable=False)
    hashed_password = sql.Column(sql.String, nullable=False)
    created_at = sql.Column(sql.DateTime, default=datetime.datetime.now)

    roles = sql.orm.relationship("Role", secondary=user_roles, back_populates="users")

# Povezana na role usere user_roles i na permisije preko role_permissions
class Role(Base):
    __tablename__ = 'roles'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String(100), unique=True, nullable=False)
    description = sql.Column(sql.String(1000), unique=False, nullable=True)

    users = sql.orm.relationship("User", secondary=user_roles, back_populates="roles")
    permissions = sql.orm.relationship("Permission", secondary=role_permissions, back_populates="roles")

#Povezana na role preko role_permissions
class Permission(Base):
    __tablename__ = 'permissions'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    name = sql.Column(sql.String(100), unique=True, nullable=False)
    description = sql.Column(sql.String(1000), unique=False, nullable=True)

    roles = sql.orm.relationship("Role", secondary=role_permissions, back_populates="permissions")


if __name__ == "__main__":
    print("Creating tables from models.py...")
    Base.metadata.create_all(bind=database.engine)
    print("Tables created.")