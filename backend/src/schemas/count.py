from pydantic import BaseModel,Field,model_validator
class CountInput(BaseModel):
 a:int=Field(ge=0,le=500,strict=True)
 b:int=Field(ge=0,le=500,strict=True)
 c:int=Field(ge=0,le=500,strict=True)
 d:int=Field(ge=0,le=500,strict=True)
 source:str=Field(default='',max_length=160)
 @model_validator(mode='after')
 def total(self):
  if not 1<=self.a+self.b+self.c+self.d<=1000:raise ValueError('每层总量须为1..1000')
  return self
