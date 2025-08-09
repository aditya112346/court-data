from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime
from datetime import datetime

Base = declarative_base()

class QueryLog(Base):
    __tablename__ = 'query_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_type: Mapped[str] = mapped_column(String(50))
    case_number: Mapped[str] = mapped_column(String(50))
    filing_year: Mapped[str] = mapped_column(String(10))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_response: Mapped[str] = mapped_column(Text)
    parsed_json: Mapped[str] = mapped_column(Text)
