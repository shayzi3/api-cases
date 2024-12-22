from src.db.repository import ORMRepository
from src.db.models import Item
from src.schemas import ItemSchema


class ItemRepository(ORMRepository[ItemSchema]):
     model = Item