from datetime import datetime
from sqlalchemy import String,ForeignKey,Double,JSON,DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class AssociationRun(Base):
 __tablename__='association_runs'
 id:Mapped[int]=mapped_column(primary_key=True)
 name:Mapped[str]=mapped_column(String(160),unique=True)
 study_id:Mapped[int]=mapped_column(ForeignKey('association_studies.id'))
 alpha:Mapped[float]=mapped_column(Double(asdecimal=False),default=.05)
 status:Mapped[str]=mapped_column(String(20),default='queued')
 input_snapshot:Mapped[dict]=mapped_column(JSON,default=dict)
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(String(700),default='')
 created_by:Mapped[int]=mapped_column(ForeignKey('users.id'))
 created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
