from sqlalchemy import select
from fastapi import HTTPException
from src.models import ExposureStratum,TableCount
from src.utils.serializers import serialize
from src.utils.audit import record
from .cmh_algorithm import validate_tables
def listing(db,study_id):
 rows=db.execute(select(TableCount,ExposureStratum).join(ExposureStratum,ExposureStratum.id==TableCount.stratum_id).where(ExposureStratum.study_id==study_id).order_by(ExposureStratum.code)).all()
 raw=[{**serialize(t),'code':s.code,'name':s.name,'description':s.description} for t,s in rows]
 return validate_tables(raw) if raw else []
def save(db,id,data,user):
 if not db.get(ExposureStratum,id):raise HTTPException(404,'分层不存在')
 row=db.scalar(select(TableCount).where(TableCount.stratum_id==id))
 if not row:row=TableCount(stratum_id=id,**data.model_dump());db.add(row)
 else:
  for k,v in data.model_dump().items():setattr(row,k,v)
 db.flush();record(db,user,'count.saved',row.id);db.commit();return serialize(row)
