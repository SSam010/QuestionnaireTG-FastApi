from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_link: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    investment_time: Mapped[str] = mapped_column(String, nullable=False)
    investment_tools: Mapped[str] = mapped_column(String, nullable=False)
    investment_amount: Mapped[str] = mapped_column(String, nullable=False)
    meeting: Mapped[str] = mapped_column(String, nullable=False)
    contact_number: Mapped[str] = mapped_column(String, nullable=False)
    registered_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

