from src.db.repository import ORMRepository
from src.db.models import Case
from src.schemas.api_v1 import CaseSchema


class CaseRepository(ORMRepository[CaseSchema]):
     model = Case