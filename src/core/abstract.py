
from abc import ABC, abstractmethod


class Crud(ABC):
     
     @abstractmethod
     def create(model, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def read(model, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def update(model, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def delete(model, **extras):
          raise NotImplementedError()