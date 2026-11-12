from sqlalchemy import select
from fastapi import HTTPException
from src.models import AssociationStudy
from src.utils.serializers import serialize
from src.utils.audit import record
def listing(db):return [serialize(x) for x in db.scalars(select(AssociationStudy).order_by(AssociationStudy.id))]
def create(db,data,user):
 if db.scalar(select(AssociationStudy).where(AssociationStudy.code==data.code)):raise HTTPException(409,'研究编号重复')
 row=AssociationStudy(**data.model_dump());db.add(row);db.flush();record(db,user,'study.created',row.id);db.commit();return serialize(row)
def patch(db,id,data,user):
 row=db.get(AssociationStudy,id)
 if not row:raise HTTPException(404,'研究不存在')
 row.description=data.description;record(db,user,'study.annotated',id);db.commit();return serialize(row)
