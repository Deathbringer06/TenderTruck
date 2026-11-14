from uuid import UUID

from pydantic import BaseModel


class ContractData(BaseModel):
    tender_id: UUID
    tender_title: str
    amount: int
    customer_name: str
    carrier_name: str
    carrier_inn: str
