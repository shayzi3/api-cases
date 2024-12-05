from __future__ import annotations


from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
     pass


class User(Base):
     __tablename__ = 'users'
     
     id: Mapped[int] = mapped_column(primary_key=True)
     email: Mapped[str] = mapped_column(nullable=False)
     password: Mapped[str] = mapped_column(nullable=False)
     cash: Mapped[float] = mapped_column(nullable=False)
     low_chanse: Mapped[float] = mapped_column(nullable=False)
     high_chanse: Mapped[float] = mapped_column(nullable=False)
     
     inventory: Mapped[List[Item]] = relationship()
     
     
class Case(Base):
     __tablename__ = 'cases'
     
     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[int] = mapped_column(nullable=False)
     image: Mapped[str] = mapped_column(nullable=False)
     
     items: Mapped[List[Item]] = relationship()
     
     
class Item(Base):
     __tablename__ = 'items'
     
     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(primary_key=True)
     price: Mapped[float] = mapped_column(primary_key=True)
     
     
     