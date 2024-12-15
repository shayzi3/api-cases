
from src.db.models import OrmBasedClassMixin, User, Item, Case
from src.schemas import UserSchema, CaseSchema, ItemSchema


class UserOrmBasedClass(OrmBasedClassMixin[UserSchema]):
     model = User
     
     
class CaseOrmBasedClass(OrmBasedClassMixin[CaseSchema]):
     model = Case
     
     
class ItemOrmBasedClass(OrmBasedClassMixin[ItemSchema]):
     model = Item
     
     
user_orm = UserOrmBasedClass()
case_orm = CaseOrmBasedClass()
item_orm = ItemOrmBasedClass()
     
     