from pydantic import BaseModel,Field
class StudyInput(BaseModel):
 code:str=Field(min_length=2,max_length=40,pattern=r'^[A-Z0-9-]+$')
 name:str=Field(min_length=3,max_length=120)
 period:str=Field(min_length=3,max_length=60)
 description:str=Field(default='',max_length=1600)
class StudyPatch(BaseModel):
 description:str=Field(max_length=1600)
