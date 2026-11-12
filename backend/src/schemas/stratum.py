from pydantic import BaseModel,Field
class StratumInput(BaseModel):
 study_id:int=Field(gt=0,strict=True)
 code:str=Field(min_length=2,max_length=40,pattern=r'^[A-Z0-9-]+$')
 name:str=Field(min_length=2,max_length=120)
 description:str=Field(default='',max_length=1200)
