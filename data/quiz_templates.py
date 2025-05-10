import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Quiz_templates(SqlAlchemyBase):
    __tablename__ = 'quiz_templates'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')