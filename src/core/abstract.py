
from abc import ABC, abstractmethod


class Crud(ABC):
     
     @abstractmethod
     def create(session, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def read(session, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def update(session, **extras):
          raise NotImplementedError()
     
     
     @abstractmethod
     def delete(session, **extras):
          raise NotImplementedError()