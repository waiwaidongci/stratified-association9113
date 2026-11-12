from datetime import datetime
from sqlalchemy import String,ForeignKey,Double,JSON,DateTime,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class AssociationStudy(Base):
 __tablename__='association_studies'
 id:Mapped[int]=mapped_column(primary_key=True)
 code:Mapped[str]=mapped_column(String(40),unique=True)
 name:Mapped[str]=mapped_column(String(120))
 period:Mapped[str]=mapped_column(String(60))
 description:Mapped[str]=mapped_column(String(1600),default='')
