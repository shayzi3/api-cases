from __future__ import annotations

from datetime import datetime
from typing import Any
from sqlalchemy import ForeignKey, func, Table, Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from src.schemas import UserSchema, CaseSchema, ItemSchema




class Base(AsyncAttrs, DeclarativeBase):
     pass




assotiation = Table(
     'assotiation',
     Base.metadata,
     Column('user_id', String, ForeignKey('users.id')),
     Column('case_id', String, ForeignKey('cases.id')),
     Column('items_id', String, ForeignKey('items.id'))
)
     

class User(Base):
     __tablename__ = 'users'
     
     id: Mapped[str] = mapped_column(primary_key=True, unique=True)
     username: Mapped[str] = mapped_column(nullable=False, unique=True)
     email: Mapped[str] = mapped_column(nullable=False)
     password: Mapped[str] = mapped_column(nullable=False)
     cash: Mapped[float] = mapped_column(nullable=False)
     low_chanse: Mapped[int] = mapped_column(nullable=False)
     high_chanse: Mapped[float] = mapped_column(nullable=False)
     created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
     is_verifed: Mapped[bool] = mapped_column(nullable=False)
     
     inventory: Mapped[list[Item]] = relationship(
         back_populates='item_users',
         uselist=True,
         lazy='joined',
         secondary=assotiation,
         overlaps='item_users'
     )
     
     
     @staticmethod
     def to_pydantic_model(model: User, *args) -> UserSchema | list[Any]:
          schema = UserSchema(
               id=model.id,
               email=model.email,
               username=model.username,
               cash=model.cash,
               created_at=model.created_at,
               inventory=model.inventory,
               is_verifed=model.is_verifed
          )
          if args:
               return [schema.__dict__.get(key) for key in args]
          return schema
               
     
     
class Case(Base):
     __tablename__ = 'cases'
     
     id: Mapped[str] = mapped_column(primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[int] = mapped_column(nullable=False)
     image: Mapped[str] = mapped_column(nullable=False)
     created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
     
     case_items: Mapped[list[Item]] = relationship(
          back_populates='item_cases',
          uselist=True,
          lazy='joined',
          secondary=assotiation,
          overlaps='inventory'
     )
     
     
     
class Item(Base):
     __tablename__ = 'items'
     
     id: Mapped[str] = mapped_column(primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[float] = mapped_column(nullable=False)
     quality: Mapped[str] = mapped_column(nullable=False)
     
     item_users: Mapped[list[User]] = relationship(
          back_populates='inventory',
          uselist=True,
          lazy='joined',
          secondary=assotiation,
          overlaps='case_items'
     )
     item_cases: Mapped[list[Case]] = relationship(
          back_populates='case_items',
          uselist=True,
          lazy='joined',
          secondary=assotiation,
          overlaps='inventory,item_users'
     )