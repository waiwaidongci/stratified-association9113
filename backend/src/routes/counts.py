from fastapi import APIRouter,Depends,HTTPException
from src.config.database import session
from src.middlewares.auth import require
from src.constants.enums import Role
from src.schemas.count import CountInput
from src.controllers.count_controller import listing,save
router=APIRouter(prefix='/counts')
@router.get('')
def index(study_id:int,db=Depends(session),u=Depends(require(Role.ADMIN,Role.ANALYST,Role.VIEWER))):return listing(db,study_id)
@router.put('/{stratum_id}')
def update(stratum_id:int,data:CountInput,db=Depends(session),u=Depends(require(Role.ADMIN,Role.ANALYST))):return save(db,stratum_id,data,u)
