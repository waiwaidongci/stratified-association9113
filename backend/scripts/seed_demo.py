from sqlalchemy import select,func
from src.config.database import Base,engine,SessionLocal
from src.models import User,AssociationStudy,ExposureStratum,TableCount,AssociationRun,VerificationNote
from src.utils.security import hash_password
from src.services.run_service import snapshot
from src.services.analysis_algorithm import analyze

def seed():
 Base.metadata.create_all(engine)
 with SessionLocal() as db:
  for role,name in [('admin','岑禾'),('analyst','岸栩'),('viewer','林澄')]:
   email=role+'@cenan.demo'
   if not db.scalar(select(User).where(User.email==email)):db.add(User(email=email,name=name,role=role,password_hash=hash_password('Cenan2026!')))
  db.flush()
  fixtures=[('CN-REV','湿度构成不同 · 总体率反转',[(18,2,80,20),(20,80,2,18)]),('CN-SPARSE','稀疏层 · 条件分布对照',[(4,1,1,4),(1,4,4,1),(0,6,2,4),(3,3,3,3)]),('CN-NULL','同率与无信息层',[(5,5,10,10),(12,12,8,8),(0,0,6,4)])]
  for code,name,tables in fixtures:
   study=db.scalar(select(AssociationStudy).where(AssociationStudy.code==code))
   if not study:study=AssociationStudy(code=code,name=name,period='2026-11 封装浸湿试验',description='匿名独立封装试片；a/b为A成功/失败，c/d为B成功/失败。湿度层在试验前声明，不依据结果切层。');db.add(study);db.flush()
   for i,values in enumerate(tables):
    sid=code+'-'+str(i+1);s=db.scalar(select(ExposureStratum).where(ExposureStratum.study_id==study.id,ExposureStratum.code==sid))
    if not s:s=ExposureStratum(study_id=study.id,code=sid,name=['低湿度层','高湿度层','边界层','复核层'][i],description='预先分层，独立试片；未声称随机分配封装。');db.add(s);db.flush()
    if not db.scalar(select(TableCount).where(TableCount.stratum_id==s.id)):db.add(TableCount(stratum_id=s.id,**dict(zip(['a','b','c','d'],values)),source='CN_20261112_封装分层计数.csv'))
  db.commit();user=db.scalar(select(User).where(User.role=='analyst'));study=db.scalar(select(AssociationStudy).where(AssociationStudy.code=='CN-REV'))
  run=db.scalar(select(AssociationRun).where(AssociationRun.name=='湿度构成 · 首轮分层核对'))
  if not run:
   snap=snapshot(db,study.id);run=AssociationRun(name='湿度构成 · 首轮分层核对',study_id=study.id,alpha=.05,created_by=user.id,input_snapshot=snap,result=analyze(snap,.05),status='completed');db.add(run);db.flush()
  if not db.scalar(select(VerificationNote).where(VerificationNote.title=='先分层，再讨论总体率')):db.add(VerificationNote(title='先分层，再讨论总体率',run_id=run.id,interpretation='两层内A成功率均较高，但样本湿度构成不同导致总体率方向相反。共同OR是分层加权摘要，不是封装因果效果。',action='保留各湿度层独立重复试片，按预先方案核对封装和浸湿时间。',status='approved',approved_by='admin@cenan.demo',review_comment='统计层边际与精确双侧定义已核对，批准独立复验记录。',created_by=user.id))
  db.commit();print({t.__tablename__:db.scalar(select(func.count()).select_from(t)) for t in [User,AssociationStudy,ExposureStratum,TableCount,AssociationRun,VerificationNote]})
if __name__=='__main__':seed()
