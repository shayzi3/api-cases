from typing import Any, Callable




def cache(class_: type) -> Callable[[Any], type]:
     cached = {}
     
     def wrapper(*args, **kwargs) -> type:
          if class_.__name__ not in cached:
               cached[class_.__name__] = class_(*args, **kwargs)
          return cached[class_.__name__]
     return wrapper


@cache
class Stack:
     cached = {}
     
     @classmethod
     def set(cls, key: str, value: Any) -> None:
          if isinstance(key, int):
               key = str(key)
          cls.cached[key] = value
          
     @classmethod
     def delete(cls, key: str) -> Any:
          if isinstance(key, int):
               key = str(key)
          
          if key in cls.cached.keys():
               return cls.cached.pop(key)
          
     @classmethod
     def get(cls, key: str) -> Any:
          if isinstance(key, int):
               key = str(key)
          return cls.cached.get(key)
     
     @classmethod
     def __str__(cls) -> str:
          return f'Stack({cls.cached})'