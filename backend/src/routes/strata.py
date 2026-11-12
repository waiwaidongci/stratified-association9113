from fastapi import APIRouter,Depends,HTTPException
from src.config.database import session
from src.middlewares.auth import require
from src.constants.enums import Role
from src.schemas.stratum import StratumInput
from src.controllers.stratum_controller import listing,create
router=APIRouter(prefix='/strata')
@router.get('')
def index(study_id:int,db=Depends(session),u=Depends(require(Role.ADMIN,Role.ANALYST,Role.VIEWER))):return listing(db,study_id)
@router.post('',status_code=201)
def add(data:StratumInput,db=Depends(session),u=Depends(require(Role.ADMIN,Role.ANALYST))):return create(db,data,u)
