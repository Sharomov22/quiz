import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Rooms(SqlAlchemyBase):
    __tablename__ = 'rooms'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    host_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    template_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("quiz_templates.id"))
    members_ids = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_only_authorized = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    assessment_json = sqlalchemy.Column(sqlalchemy.JSON, default={2: 50, 3: 70, 4: 85})
    unique_tag = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User')