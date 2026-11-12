from src.models import Audit
def record(db,user,action,target):
    db.add(Audit(actor=user.email if user is not None else 'worker',action=action,target=str(target)))
