from datetime import datetime
from sqlalchemy import String,ForeignKey,Double,JSON,DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class TableCount(Base):
 __tablename__='table_counts'
 id:Mapped[int]=mapped_column(primary_key=True)
 stratum_id:Mapped[int]=mapped_column(ForeignKey('exposure_strata.id'),unique=True)
 a:Mapped[int]=mapped_column()
 b:Mapped[int]=mapped_column()
 c:Mapped[int]=mapped_column()
 d:Mapped[int]=mapped_column()
 source:Mapped[str]=mapped_column(String(160),default='')
