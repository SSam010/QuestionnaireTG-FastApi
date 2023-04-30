from pydantic import BaseModel


class ClientCreate(BaseModel):
    tg_id: int
    tg_link: str
    name: str
    investment_time: str
    investment_tools: str
    investment_amount: str
    meeting: str
    contact_number: str


class ClientUpdate(BaseModel):
    name: str
    investment_time: str
    investment_tools: str
    investment_amount: str
    meeting: str
    contact_number: str
    is_processed: bool


class ClientUpdateProcessed(BaseModel):
    is_processed: bool
