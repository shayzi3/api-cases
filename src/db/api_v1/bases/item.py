from src.db.api_v1.repository import ORMRepository
from src.db.api_v1.models import Item
from src.schemas.api_v1 import ItemSchema


class ItemRepository(ORMRepository[ItemSchema]):
     model = Item