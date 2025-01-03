from src.db.api_v1.repository import ORMRepository
from src.db.api_v1.models import Case
from src.schemas.api_v1 import CaseSchema


class CaseRepository(ORMRepository[CaseSchema]):
     model = Case