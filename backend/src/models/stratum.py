from datetime import datetime
from sqlalchemy import String,ForeignKey,Double,JSON,DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ExposureStratum(Base):
 __tablename__='exposure_strata'
 __table_args__=(UniqueConstraint('study_id','code'),)
 id:Mapped[int]=mapped_column(primary_key=True)
 study_id:Mapped[int]=mapped_column(ForeignKey('association_studies.id'))
 code:Mapped[str]=mapped_column(String(40))
 name:Mapped[str]=mapped_column(String(120))
 description:Mapped[str]=mapped_column(String(1200),default='')
