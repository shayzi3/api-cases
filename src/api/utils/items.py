from typing_extensions import Self, Any


class ItemsGetBy:
     __slots__ = ("__data",)
     
     def __init__(self):
          self.__data = {}
          
     def get_by(
          self,
          id: str | None = None,
          name: str | None = None,
     ) -> Self:
          self.__data = {"id": id} if id else {"name": name}
          
          if (id is None) and (name is None):
               return {}
          return self
     
     
     @property
     def data_value(self) -> str | None:
          """{id: 123} -> item:123"""
          
          if self.__data:
               return f"item:{list(self.data.values())[0]}"
          
          
     @property
     def data(self) -> dict[str, Any]:
          return self.__data
          