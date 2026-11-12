from pydantic import BaseModel,Field
class RunInput(BaseModel):
 name:str=Field(min_length=3,max_length=160)
 study_id:int=Field(gt=0,strict=True)
 alpha:float=Field(default=.05,ge=.001,le=.1,strict=True,allow_inf_nan=False)
