from src.db.repository import ORMRepository
from src.db.models import Item
from src.schemas.api_v1 import ItemSchema


class ItemRepository(ORMRepository[ItemSchema]):
     model = Item