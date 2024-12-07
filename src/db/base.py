
from src.db.models import OrmBasedClassMixin, User, Item, Case


class UserOrmBasedClass(OrmBasedClassMixin):
     model = User
     
     
class CaseOrmBasedClass(OrmBasedClassMixin):
     model = Case
     
     
class ItemOrmBasedClass(OrmBasedClassMixin):
     model = Item
     
     
user_orm = UserOrmBasedClass()
case_orm = CaseOrmBasedClass()
item_orm = ItemOrmBasedClass()
     
     