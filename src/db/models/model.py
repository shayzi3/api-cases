from __future__ import annotations

from datetime import datetime
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs



class Base(AsyncAttrs, DeclarativeBase):
     pass


class User(Base):
     __tablename__ = 'users'
     
     id: Mapped[int] = mapped_column(primary_key=True, unique=True)
     email: Mapped[str] = mapped_column(nullable=False)
     password: Mapped[str] = mapped_column(nullable=False)
     cash: Mapped[float] = mapped_column(nullable=False)
     low_chanse: Mapped[float] = mapped_column(nullable=False)
     high_chanse: Mapped[float] = mapped_column(nullable=False)
     created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
     is_vetifed: Mapped[bool] = mapped_column(nullable=False)
     
     inventory: Mapped[List[Item]] = relationship(cascade='all, delete-orphan')
     
     
class Case(Base):
     __tablename__ = 'cases'
     
     id: Mapped[int] = mapped_column(primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[int] = mapped_column(nullable=False)
     image: Mapped[str] = mapped_column(nullable=False)
     created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
     
     items: Mapped[List[Item]] = relationship(cascade='all, delete-orphan')
     
     
class Item(Base):
     __tablename__ = 'items'
     
     id: Mapped[int] = mapped_column(primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(primary_key=True)
     price: Mapped[float] = mapped_column(primary_key=True)
     
     