from sqlalchemy import select
from fastapi import HTTPException
from src.models import AssociationStudy,ExposureStratum,TableCount,AssociationRun
from src.config.queue import queue
from src.utils.audit import record
from src.utils.serializers import serialize
from .analysis_algorithm import analyze
from .cmh_algorithm import validate_tables
QUEUE='cenan:runs'
def listing(db):
 rows=[]
 for x in db.scalars(select(AssociationRun).order_by(AssociationRun.id.desc())):
  r=serialize(x);r.pop('result');r.pop('input_snapshot');rows.append(r)
 return rows

def snapshot(db,id):
 study=db.get(AssociationStudy,id)
 if not study:raise HTTPException(404,'研究不存在')
 strata=db.scalars(select(ExposureStratum).where(ExposureStratum.study_id==id).order_by(ExposureStratum.code)).all()
 if not 2<=len(strata)<=8:raise HTTPException(422,'需要2..8个完整分层')
 tables=[]
 for s in strata:
  t=db.scalar(select(TableCount).where(TableCount.stratum_id==s.id))
  if not t:raise HTTPException(422,'每层必须有2×2计数')
  tables.append({**serialize(t),'code':s.code,'name':s.name,'description':s.description})
 validate_tables(tables);return {'study':serialize(study),'tables':tables}
def create(db,data,user):
 if db.scalar(select(AssociationRun).where(AssociationRun.name==data.name)):raise HTTPException(409,'研究名称重复')
 snap=snapshot(db,data.study_id);row=AssociationRun(**data.model_dump(),created_by=user.id,input_snapshot=snap);db.add(row);db.flush();record(db,user,'run.queued',row.id);db.commit();queue.rpush(QUEUE,str(row.id));return serialize(row)
def compute(db,id):
 row=db.get(AssociationRun,id)
 if not row or row.status not in ['queued','running']:return
 row.status='running';db.commit();row.result=analyze(row.input_snapshot,row.alpha);row.status='completed';row.error='';record(db,None,'worker.completed',row.id);db.commit();return serialize(row)
